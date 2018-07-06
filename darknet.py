from mxnet.gluon import nn
from utils import *


def ConvBNBlock(channels, kernel_size, strides, pad, use_bias=False, leaky=True):
    blk = nn.Sequential()
    blk.add(nn.Conv2D(int(channels), kernel_size=kernel_size, strides=strides, padding=pad,
                      use_bias=use_bias))
    if not use_bias:
        blk.add(nn.BatchNorm(in_channels=int(channels)))
    if leaky:
        blk.add(nn.LeakyReLU(0.1))
    return blk


class ShortCutBlock(nn.Block):
    def __init__(self, channels):
        super(ShortCutBlock, self).__init__()
        self.conv_1 = ConvBNBlock(channels / 2, 1, 1, 0)
        self.conv_2 = ConvBNBlock(channels, 3, 1, 1)

    def forward(self, x, *args):
        blk = self.conv_1(x)
        blk = self.conv_2(blk)
        return blk + x


class UpSampleBlock(nn.Block):
    def __init__(self, scale, sample_type="nearest"):
        super(UpSampleBlock, self).__init__()
        self.scale = scale
        self.sample_type = sample_type

    def forward(self, x):
        return nd.UpSampling(x, scale=self.scale, sample_type=self.sample_type)


class DarkNet(nn.Block):
    def __init__(self, num_classes=80, input_dim=416):
        super(DarkNet, self).__init__()
        self.num_classes = num_classes
        self.input_dim = input_dim
        self.anchors = [(10, 13), (16, 30), (33, 23), (30, 61), (62, 45),
                        (59, 119), (116, 90), (156, 198), (373, 326)]

        self.conv_bn_block_0 = ConvBNBlock(32, 3, 1, 1)
        self.conv_bn_block_1 = ConvBNBlock(64, 3, 2, 1)
        self.shortcut_block_4 = ShortCutBlock(64)
        self.conv_bn_block_5 = ConvBNBlock(128, 3, 2, 1)
        self.shortcut_block_8 = ShortCutBlock(128)
        self.shortcut_block_11 = ShortCutBlock(128)
        self.conv_bn_block_12 = ConvBNBlock(256, 3, 2, 1)
        self.shortcut_block_15 = ShortCutBlock(256)
        self.shortcut_block_18 = ShortCutBlock(256)
        self.shortcut_block_21 = ShortCutBlock(256)
        self.shortcut_block_24 = ShortCutBlock(256)
        self.shortcut_block_27 = ShortCutBlock(256)
        self.shortcut_block_30 = ShortCutBlock(256)
        self.shortcut_block_33 = ShortCutBlock(256)
        self.shortcut_block_36 = ShortCutBlock(256)
        self.conv_bn_block_37 = ConvBNBlock(512, 3, 2, 1)
        self.shortcut_block_40 = ShortCutBlock(512)
        self.shortcut_block_43 = ShortCutBlock(512)
        self.shortcut_block_46 = ShortCutBlock(512)
        self.shortcut_block_49 = ShortCutBlock(512)
        self.shortcut_block_52 = ShortCutBlock(512)
        self.shortcut_block_55 = ShortCutBlock(512)
        self.shortcut_block_58 = ShortCutBlock(512)
        self.shortcut_block_61 = ShortCutBlock(512)
        self.conv_bn_block_62 = ConvBNBlock(1024, 3, 2, 1)
        self.shortcut_block_65 = ShortCutBlock(1024)
        self.shortcut_block_68 = ShortCutBlock(1024)
        self.shortcut_block_71 = ShortCutBlock(1024)
        self.shortcut_block_74 = ShortCutBlock(1024)
        self.conv_bn_block_75 = ConvBNBlock(512, 1, 1, 0)
        self.conv_bn_block_76 = ConvBNBlock(1024, 3, 1, 1)
        self.conv_bn_block_77 = ConvBNBlock(512, 1, 1, 0)
        self.conv_bn_block_78 = ConvBNBlock(1024, 3, 1, 1)
        self.conv_bn_block_79 = ConvBNBlock(512, 1, 1, 0)
        self.conv_bn_block_80 = ConvBNBlock(1024, 3, 1, 1)
        self.conv_bn_block_81 = ConvBNBlock(3 * (5+self.num_classes), 1, 1, 0, use_bias=True, leaky=False)
        self.conv_bn_block_84 = ConvBNBlock(256, 1, 1, 0)
        self.upsample_block_85 = UpSampleBlock(scale=2)
        self.conv_bn_block_87 = ConvBNBlock(256, 1, 1, 0)
        self.conv_bn_block_88 = ConvBNBlock(512, 3, 1, 1)
        self.conv_bn_block_89 = ConvBNBlock(256, 1, 1, 0)
        self.conv_bn_block_90 = ConvBNBlock(512, 3, 1, 1)
        self.conv_bn_block_91 = ConvBNBlock(256, 1, 1, 0)
        self.conv_bn_block_92 = ConvBNBlock(512, 3, 1, 1)
        self.conv_bn_block_93 = ConvBNBlock(3 * (5+self.num_classes), 1, 1, 0, use_bias=True, leaky=False)
        self.conv_bn_block_96 = ConvBNBlock(128, 1, 1, 0)
        self.upsample_block_97 = UpSampleBlock(scale=2)
        self.conv_bn_block_99 = ConvBNBlock(128, 1, 1, 0)
        self.conv_bn_block_100 = ConvBNBlock(256, 3, 1, 1)
        self.conv_bn_block_101 = ConvBNBlock(128, 1, 1, 0)
        self.conv_bn_block_102 = ConvBNBlock(256, 3, 1, 1)
        self.conv_bn_block_103 = ConvBNBlock(128, 1, 1, 0)
        self.conv_bn_block_104 = ConvBNBlock(256, 3, 1, 1)
        self.conv_bn_block_105 = ConvBNBlock(3 * (5+self.num_classes), 1, 1, 0, use_bias=True, leaky=False)

    def forward(self, x):
        # modules = self.conv_bn_block_0._children
        # i = 0
        # tmp = x.copy()
        # for block_name in modules:
        #     module = modules.get(block_name)
        #     tmp = module(tmp)
        #     t = np.load("data/pytorch_{}.npy".format(i))
        #     i += 1
        #     print(nd.sum(tmp - nd.array(t)))
        conv_0 = self.conv_bn_block_0(x)
        conv_0 = self.conv_bn_block_1(conv_0)
        conv_0 = self.shortcut_block_4(conv_0)
        conv_0 = self.conv_bn_block_5(conv_0)
        conv_0 = self.shortcut_block_8(conv_0)
        conv_0 = self.shortcut_block_11(conv_0)
        conv_0 = self.conv_bn_block_12(conv_0)
        conv_0 = self.shortcut_block_15(conv_0)
        conv_0 = self.shortcut_block_18(conv_0)
        conv_0 = self.shortcut_block_21(conv_0)
        conv_0 = self.shortcut_block_24(conv_0)
        conv_0 = self.shortcut_block_27(conv_0)
        conv_0 = self.shortcut_block_30(conv_0)
        conv_0 = self.shortcut_block_33(conv_0)
        shortcut_36 = self.shortcut_block_36(conv_0)
        conv_0 = self.conv_bn_block_37(conv_0)
        conv_0 = self.shortcut_block_40(conv_0)
        conv_0 = self.shortcut_block_43(conv_0)
        conv_0 = self.shortcut_block_46(conv_0)
        conv_0 = self.shortcut_block_49(conv_0)
        conv_0 = self.shortcut_block_52(conv_0)
        conv_0 = self.shortcut_block_55(conv_0)
        conv_0 = self.shortcut_block_58(conv_0)
        shortcut_61 = self.shortcut_block_61(conv_0)
        conv_0 = self.conv_bn_block_62(shortcut_61)
        conv_0 = self.shortcut_block_65(conv_0)
        conv_0 = self.shortcut_block_68(conv_0)
        conv_0 = self.shortcut_block_71(conv_0)
        conv_0 = self.shortcut_block_74(conv_0)
        conv_0 = self.conv_bn_block_75(conv_0)
        conv_0 = self.conv_bn_block_76(conv_0)
        conv_0 = self.conv_bn_block_77(conv_0)
        conv_78 = self.conv_bn_block_78(conv_0)
        conv_79 = self.conv_bn_block_79(conv_78)
        conv_80 = self.conv_bn_block_80(conv_79)
        conv_81 = self.conv_bn_block_81(conv_80)

        predict_82 = train_transform(conv_81, self.num_classes, 13)
        detections = predict_82

        route_83 = conv_79.copy()
        conv_84 = self.conv_bn_block_84(route_83)
        upsample_85 = self.upsample_block_85(conv_84)
        route_86 = nd.concat(upsample_85, shortcut_61, dim=1)

        conv_87 = self.conv_bn_block_87(route_86)
        conv_88 = self.conv_bn_block_88(conv_87)
        conv_89 = self.conv_bn_block_89(conv_88)
        conv_90 = self.conv_bn_block_90(conv_89)
        conv_91 = self.conv_bn_block_91(conv_90)
        conv_92 = self.conv_bn_block_92(conv_91)
        conv_93 = self.conv_bn_block_93(conv_92)

        # tmp_anchors = [self.anchors[i] for i in (3, 4, 5)]
        # predict_94 = predict_transform(conv_93, self.input_dim, tmp_anchors, self.num_classes)
        # detections = nd.concat(detections, predict_94, dim=1)
        # predict_94 = nn.Flatten()(conv_93)
        predict_94 = train_transform(conv_93, self.num_classes, 26)
        detections = nd.concat(detections, predict_94, dim=1)
        # predict_94 = conv_93.copy()

        route_95 = conv_91.copy()
        conv_96 = self.conv_bn_block_96(route_95)
        upsample_97 = self.upsample_block_97(conv_96)
        route_98 = nd.concat(upsample_97, shortcut_36, dim=1)

        conv_99 = self.conv_bn_block_99(route_98)
        conv_100 = self.conv_bn_block_100(conv_99)
        conv_101 = self.conv_bn_block_101(conv_100)
        conv_102 = self.conv_bn_block_102(conv_101)
        conv_103 = self.conv_bn_block_103(conv_102)
        conv_104 = self.conv_bn_block_104(conv_103)
        conv_105 = self.conv_bn_block_105(conv_104)

        # tmp_anchors = [self.anchors[i] for i in (0, 1, 2)]
        # predict_106 = predict_transform(conv_105, self.input_dim, tmp_anchors, self.num_classes)
        # detections = nd.concat(detections, predict_106, dim=1)
        # predict_106 = nn.Flatten()(conv_105)
        predict_106 = train_transform(conv_105, self.num_classes, 52)
        detections = nd.concat(detections, predict_106, dim=1)
        # predict_106 = conv_105.copy()
        return detections

    def load_weights(self, weightfile, fine_tune):
        # Open the weights file
        fp = open(weightfile, "rb")

        # The first 5 values are header information
        # 1. Major version number
        # 2. Minor Version Number
        # 3. Subversion number
        # 4,5. Images seen by the network (during training)
        self.header = nd.array(np.fromfile(fp, dtype=np.int32, count=5))
        self.seen = self.header[3]

        weights = nd.array(np.fromfile(fp, dtype=np.float32))
        ptr = 0

        def set_data(model, ptr):
            conv = model[0]
            if len(model) > 1:
                bn = model[1]

                # Get the number of weights of Batch Norm Layer
                num_bn_beta = self.numel(bn.beta.shape)
                # Load the weights
                bn_beta = weights[ptr:ptr + num_bn_beta]
                ptr += num_bn_beta

                bn_gamma = weights[ptr: ptr + num_bn_beta]
                ptr += num_bn_beta

                bn_running_mean = weights[ptr: ptr + num_bn_beta]
                ptr += num_bn_beta

                bn_running_var = weights[ptr: ptr + num_bn_beta]
                ptr += num_bn_beta

                # Cast the loaded weights into dims of model weights.
                bn_beta = bn_beta.reshape(bn.beta.shape)
                bn_gamma = bn_gamma.reshape(bn.gamma.shape)
                bn_running_mean = bn_running_mean.reshape(bn.running_mean.shape)
                bn_running_var = bn_running_var.reshape(bn.running_var.shape)

                bn.gamma.set_data(bn_gamma)
                bn.beta.set_data(bn_beta)
                bn.running_mean.set_data(bn_running_mean)
                bn.running_var.set_data(bn_running_var)
            else:
                num_biases = self.numel(conv.bias.shape)

                conv_biases = weights[ptr: ptr + num_biases]
                ptr = ptr + num_biases

                conv_biases = conv_biases.reshape(conv.bias.shape)

                conv.bias.set_data(conv_biases)

            num_weights = self.numel(conv.weight.shape)

            conv_weights = weights[ptr:ptr + num_weights]
            ptr = ptr + num_weights

            conv_weights = conv_weights.reshape(conv.weight.shape)

            conv.weight.set_data(conv_weights)
            return ptr

        modules = self._children
        for block_name in modules:
            if fine_tune:
                if block_name.find("81") != -1:
                    ptr = 56629087
                    continue
                elif block_name.find("93") != -1:
                    ptr = 60898910
                    continue
                elif block_name.find("105") != -1:
                    continue
            module = modules.get(block_name)
            if isinstance(module, nn.Sequential):
                ptr = set_data(module, ptr)
            elif isinstance(module, ShortCutBlock):
                shortcut_modules = module._children
                for shortcut_name in shortcut_modules:
                    ptr = set_data(shortcut_modules.get(shortcut_name), ptr)
            elif isinstance(module, UpSampleBlock):
                continue
            else:
                print("load weights wrong")

    def numel(self, x):
        if isinstance(x, nd.NDArray):
            x.asnumpy()
        return np.prod(x)


if __name__ == '__main__':
    darknet = DarkNet()
    darknet.initialize()
    X = nd.uniform(shape=(1, 3, 416, 416))
    detections = darknet(X)
    darknet.load_weights("yolov3.weights")
    print(detections.shape)