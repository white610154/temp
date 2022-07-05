from .resnetModule import BasicBlock
from .resnetModule import Bottleneck
from .resnetModule import resnet

__all__ = ['se_resnet18', 'se_resnet34', 'se_resnet50', 'se_resnet101',
           'se_resnet152', 'se_resnext50_32x4d', 'se_resnext101_32x8d',
           'se_wide_resnet50_2', 'se_wide_resnet101_2']

def se_resnet18(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return resnet('se_resnet18', BasicBlock, [2, 2, 2, 2], pretrained, progress,
                   **kwargs)

def se_resnet34(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return resnet('se_resnet34', BasicBlock, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)

def se_resnet50(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return resnet('se_resnet50', Bottleneck, [3, 4, 6, 3], pretrained, progress,
                   **kwargs)

def se_resnet101(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return resnet('se_resnet101', Bottleneck, [3, 4, 23, 3], pretrained, progress,
                   **kwargs)

def se_resnet152(pretrained=False, progress=True, **kwargs):
    kwargs['isAttention'] = 1
    return resnet('se_resnet152', Bottleneck, [3, 8, 36, 3], pretrained, progress,
                   **kwargs)

def se_resnext50_32x4d(pretrained=False, progress=True, **kwargs):
    kwargs['groups'] = 32
    kwargs['width_per_group'] = 4
    kwargs['isAttention'] = 1
    return resnet('se_resnext50_32x4d', Bottleneck, [3, 4, 6, 3],
                   pretrained, progress, **kwargs)

def se_resnext101_32x8d(pretrained=False, progress=True, **kwargs):
    kwargs['groups'] = 32
    kwargs['width_per_group'] = 8
    kwargs['isAttention'] = 1
    return resnet('se_resnext101_32x8d', Bottleneck, [3, 4, 23, 3],
                   pretrained, progress, **kwargs)

def se_wide_resnet50_2(pretrained=False, progress=True, **kwargs):
    kwargs['width_per_group'] = 64 * 2
    kwargs['isAttention'] = 1
    return resnet('se_wide_resnet50_2', Bottleneck, [3, 4, 6, 3],
                   pretrained, progress, **kwargs)

def se_wide_resnet101_2(pretrained=False, progress=True, **kwargs):
    kwargs['width_per_group'] = 64 * 2
    kwargs['isAttention'] = 1
    return resnet('se_wide_resnet101_2', Bottleneck, [3, 4, 23, 3],
                   pretrained, progress, **kwargs)