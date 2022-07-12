# -*- coding: utf-8 -*-

import torch
import torch.nn as nn
import torch.nn.functional as F
from .resnetModule import BasicBlock
from .resnetModule import Bottleneck
from .resnetModule import ChannelAttention, SpatialAttention

__all__ = ["CSP_ResNet", "csp_resnet18", "csp_resnet34", "csp_resnet50", "csp_resnet101", "csp_resnet152"
                       , "csp_se_resnet18", "csp_se_resnet34", "csp_se_resnet50", "csp_se_resnet101" , "csp_se_resnet152"
                       , "csp_cbam_resnet18", "csp_cbam_resnet34", "csp_cbam_resnet50", "csp_cbam_resnet101", "csp_cbam_resnet152"
                       , "csp_se_cbam_resnet18", "csp_se_cbam_resnet34", "csp_se_cbam_resnet50", "csp_se_cbam_resnet101", "csp_se_cbam_resnet152"
                       ]

class BN_Conv2d_Leaky(nn.Module):
    """
    BN_CONV_LeakyRELU
    """
    def __init__(self, inplanes: object, out_channels: object, kernel_size: object, stride: object, padding: object,
                 dilation=1, bias=False) -> object:
        super(BN_Conv2d_Leaky, self).__init__()
        self.seq = nn.Sequential(
            nn.Conv2d(inplanes, out_channels, kernel_size=kernel_size, stride=stride,
                      padding=padding, dilation=dilation, bias=bias),
            nn.BatchNorm2d(out_channels)
        )

    def forward(self, x):
        return F.leaky_relu(self.seq(x))


class Stem(nn.Module):
    def __init__(self, block, inplanes, num_blocks, stride=2, groups=1, width_per_group=64, isAttention=None, norm_layer=None):
        super(Stem, self).__init__()
        self.groups = groups
        self.base_width = width_per_group
        self.isAttention = isAttention
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        self._norm_layer = norm_layer
        width = int(inplanes * (width_per_group / 64.)) * groups
        self.c0 = (width // 2) * block.expansion if stride !=1 else width // 2
        self.c1 = (width - width // 2)* block.expansion if stride !=1 else width - width // 2
     
        self.inchannel = self.c1
        self.hidden_channels = inplanes
        self.out_channels = self.hidden_channels * 2 
        self.trans_part0 = nn.Sequential(BN_Conv2d_Leaky(self.c0, self.hidden_channels* block.expansion, 1, 1, 0), nn.AvgPool2d(stride))
        self.block_bone = self._make_layer(block, self.hidden_channels, num_blocks, stride)
        self.trans_part1 = BN_Conv2d_Leaky(self.hidden_channels * block.expansion, self.hidden_channels * block.expansion, 1, 1, 0)
        self.trans = BN_Conv2d_Leaky(self.out_channels* block.expansion, self.out_channels* block.expansion, 1, 1, 0)



    def _make_layer(self, block, planes, num_blocks, stride):
        downsample = None
        norm_layer = self._norm_layer
        if stride != 1 or self.inchannel != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inchannel, planes * block.expansion, kernel_size=1, stride=stride),
                norm_layer(planes * block.expansion),
            )
        layers = []
        layers.append(block(self.inchannel, planes, stride, downsample, self.groups,
                            self.base_width, norm_layer=norm_layer, isAttention=self.isAttention))
        self.inchannel = planes * block.expansion
        for _ in range(1, num_blocks):
            layers.append(block(self.inchannel, planes, groups=self.groups,
                                base_width=self.base_width, norm_layer=norm_layer, isAttention=self.isAttention))

        return nn.Sequential(*layers)


    def forward(self, x):
        x0 = x[:, :self.c0, :, :]
        x1 = x[:, self.c0:, :, :]
        out0 = self.trans_part0(x0)
        out1 = self.trans_part1(self.block_bone(x1))
        out = torch.cat((out0, out1), 1)
        return self.trans(out)


class CSP_ResNet(nn.Module):
    def __init__(self, block, layers, num_classes=1000, groups=1, width_per_group=64, isAttention=None, isCBAM=None):
        super(CSP_ResNet, self).__init__()
        self.isCBAM = isCBAM
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)

        if self.isCBAM:
            self.ca = ChannelAttention(64)
            self.sa = SpatialAttention()

        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.stem0 = Stem(block, 64, layers[0], stride=1, groups=groups, width_per_group=width_per_group, isAttention=isAttention)
        self.stem1 = Stem(block, 128, layers[1], groups=groups, width_per_group=width_per_group, isAttention=isAttention)
        self.stem2 = Stem(block, 256, layers[2], groups=groups, width_per_group=width_per_group, isAttention=isAttention)
        self.stem3 = Stem(block, 512, layers[3], groups=groups, width_per_group=width_per_group, isAttention=isAttention)

        if self.isCBAM:
            self.ca1 = ChannelAttention(groups * width_per_group * 16 * block.expansion)
            self.sa1 = SpatialAttention()

        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(groups * width_per_group * 16 * block.expansion, num_classes)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)    

    def forward(self, x):
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.maxpool(out)

        if self.isCBAM is not None:
            out = self.ca(out) * out
            out = self.sa(out) * out

        out = self.stem0(out)
        out = self.stem1(out)
        out = self.stem2(out)
        out = self.stem3(out)

        if self.isCBAM is not None:
            out = self.ca1(out) * out
            out = self.sa1(out) * out

        out = self.global_pool(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


def csp_resnet(arch, block, layer, pretrained=False, progress=True,**kwargs):
    model = CSP_ResNet(block, layer, **kwargs)
    return model

def csp_resnet18(pretrained=False, progress=True, **kwargs):
    return csp_resnet("csp_resnet18", BasicBlock, [2, 2, 2, 2], pretrained, progress,
                    **kwargs)


def csp_resnet34(pretrained=False, progress=True, **kwargs):
    return csp_resnet('csp_resnet34', BasicBlock, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)


def csp_resnet50(pretrained=False, progress=True, **kwargs):
    return csp_resnet('csp_resnet50', Bottleneck, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)


def csp_resnet101(pretrained=False, progress=True, **kwargs):
    return csp_resnet('csp_resnet101', Bottleneck, [3, 4, 23, 3], pretrained, progress,
                   **kwargs)


def csp_resnet152(pretrained=False, progress=True, **kwargs):
    return csp_resnet('csp_resnet152', Bottleneck, [3, 8, 36, 3], pretrained, progress,
                   **kwargs)

#===================================================================================================#
#                                 SE series
#===================================================================================================#

def csp_se_resnet18(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return csp_resnet("csp_se_resnet18", BasicBlock, [2, 2, 2, 2], pretrained, progress,
                    **kwargs)


def csp_se_resnet34(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return csp_resnet('csp_se_resnet34', BasicBlock, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)


def csp_se_resnet50(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return csp_resnet('csp_se_resnet50', Bottleneck, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)


def csp_se_resnet101(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return csp_resnet('csp_se_resnet101', Bottleneck, [3, 4, 23, 3], pretrained, progress,
                   **kwargs)

def csp_se_resnet152(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return csp_resnet('csp_se_resnet152', Bottleneck, [3, 8, 36, 3], pretrained, progress,
                   **kwargs)

#===================================================================================================#
#                                 CBAM series 
#===================================================================================================#

def csp_cbam_resnet18(pretrained=False, progress=True, **kwargs):
    kwargs['isCBAM'] = 1
    return csp_resnet("csp_cbam_resnet18", BasicBlock, [2, 2, 2, 2], pretrained, progress,
                    **kwargs)


def csp_cbam_resnet34(pretrained=False, progress=True, **kwargs):
    kwargs['isCBAM'] = 1
    return csp_resnet('csp_cbam_resnet34', BasicBlock, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)


def csp_cbam_resnet50(pretrained=False, progress=True, **kwargs):
    kwargs['isCBAM'] = 1
    return csp_resnet('csp_cbam_resnet50', Bottleneck, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)


def csp_cbam_resnet101(pretrained=False, progress=True, **kwargs):
    kwargs['isCBAM'] = 1
    return csp_resnet('csp_cbam_resnet101', Bottleneck, [3, 4, 23, 3], pretrained, progress,
                   **kwargs)


def csp_cbam_resnet152(pretrained=False, progress=True, **kwargs):
    kwargs['isCBAM'] = 1
    return csp_resnet('csp_cbam_resnet152', Bottleneck, [3, 8, 36, 3], pretrained, progress,
                   **kwargs)

#===================================================================================================#
#                                 SE CBAM series 
#===================================================================================================#

def csp_se_cbam_resnet18(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    kwargs['isCBAM'] = 1
    return csp_resnet("csp_se_cbam_resnet18", BasicBlock, [2, 2, 2, 2], pretrained, progress,
                    **kwargs)


def csp_se_cbam_resnet34(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    kwargs['isCBAM'] = 1
    return csp_resnet('csp_se_cbam_resnet34', BasicBlock, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)


def csp_se_cbam_resnet50(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    kwargs['isCBAM'] = 1
    return csp_resnet('csp_se_cbam_resnet50', Bottleneck, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)


def csp_se_cbam_resnet101(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    kwargs['isCBAM'] = 1
    return csp_resnet('csp_se_cbam_resnet101', Bottleneck, [3, 4, 23, 3], pretrained, progress,
                   **kwargs)


def csp_se_cbam_resnet152(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    kwargs['isCBAM'] = 1
    return csp_resnet('csp_se_cbam_resnet152', Bottleneck, [3, 8, 36, 3], pretrained, progress,
                   **kwargs)
