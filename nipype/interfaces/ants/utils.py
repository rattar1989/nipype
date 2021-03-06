# -*- coding: utf-8 -*-
"""ANTS Apply Transforms interface

   Change directory to provide relative paths for doctests
   >>> import os
   >>> filepath = os.path.dirname( os.path.realpath( __file__ ) )
   >>> datadir = os.path.realpath(os.path.join(filepath, '../../testing/data'))
   >>> os.chdir(datadir)
"""
from __future__ import print_function, division, unicode_literals, absolute_import

import os

from ...utils.filemanip import split_filename
from ..base import TraitedSpec, File, traits, isdefined, InputMultiPath
from .base import ANTSCommand, ANTSCommandInputSpec


class AverageAffineTransformInputSpec(ANTSCommandInputSpec):
    dimension = traits.Enum(3, 2, argstr='%d', usedefault=False, mandatory=True,
                            position=0, desc='image dimension (2 or 3)')
    output_affine_transform = File(argstr='%s', mandatory=True, position=1,
                                   desc='Outputfname.txt: the name of the resulting transform.')
    transforms = InputMultiPath(File(exists=True), argstr='%s', mandatory=True,
                                position=3, desc='transforms to average')


class AverageAffineTransformOutputSpec(TraitedSpec):
    affine_transform = File(exists=True, desc='average transform file')


class AverageAffineTransform(ANTSCommand):
    """
    Examples
    --------
    >>> from nipype.interfaces.ants import AverageAffineTransform
    >>> avg = AverageAffineTransform()
    >>> avg.inputs.dimension = 3
    >>> avg.inputs.transforms = ['trans.mat', 'func_to_struct.mat']
    >>> avg.inputs.output_affine_transform = 'MYtemplatewarp.mat'
    >>> avg.cmdline # doctest: +ALLOW_UNICODE
    'AverageAffineTransform 3 MYtemplatewarp.mat trans.mat func_to_struct.mat'
    """
    _cmd = 'AverageAffineTransform'
    input_spec = AverageAffineTransformInputSpec
    output_spec = AverageAffineTransformOutputSpec

    def _format_arg(self, opt, spec, val):
        return super(AverageAffineTransform, self)._format_arg(opt, spec, val)

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['affine_transform'] = os.path.abspath(
            self.inputs.output_affine_transform)
        return outputs


class AverageImagesInputSpec(ANTSCommandInputSpec):
    dimension = traits.Enum(3, 2, argstr='%d', mandatory=True,
                            position=0, desc='image dimension (2 or 3)')
    output_average_image = File("average.nii", argstr='%s', position=1, desc='the name of the resulting image.',
                                usedefault=True, hash_files=False)
    normalize = traits.Bool(argstr="%d", mandatory=True, position=2, desc='Normalize: if true, the 2nd image' +
                            'is divided by its mean. This will select the largest image to average into.')
    images = InputMultiPath(File(exists=True), argstr='%s', mandatory=True, position=3,
                            desc='image to apply transformation to (generally a coregistered functional)')


class AverageImagesOutputSpec(TraitedSpec):
    output_average_image = File(exists=True, desc='average image file')


class AverageImages(ANTSCommand):
    """
    Examples
    --------
    >>> from nipype.interfaces.ants import AverageImages
    >>> avg = AverageImages()
    >>> avg.inputs.dimension = 3
    >>> avg.inputs.output_average_image = "average.nii.gz"
    >>> avg.inputs.normalize = True
    >>> avg.inputs.images = ['rc1s1.nii', 'rc1s1.nii']
    >>> avg.cmdline # doctest: +ALLOW_UNICODE
    'AverageImages 3 average.nii.gz 1 rc1s1.nii rc1s1.nii'
    """
    _cmd = 'AverageImages'
    input_spec = AverageImagesInputSpec
    output_spec = AverageImagesOutputSpec

    def _format_arg(self, opt, spec, val):
        return super(AverageImages, self)._format_arg(opt, spec, val)

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['output_average_image'] = os.path.realpath(
            self.inputs.output_average_image)
        return outputs


class MultiplyImagesInputSpec(ANTSCommandInputSpec):
    dimension = traits.Enum(3, 2, argstr='%d', usedefault=False, mandatory=True, position=0,
                            desc='image dimension (2 or 3)')
    first_input = File(argstr='%s', exists=True, mandatory=True, position=1, desc='image 1')
    second_input = traits.Either(File(exists=True), traits.Float, argstr='%s', mandatory=True, position=2,
                                 desc='image 2 or multiplication weight')
    output_product_image = File(argstr='%s', mandatory=True, position=3,
                                desc='Outputfname.nii.gz: the name of the resulting image.')


class MultiplyImagesOutputSpec(TraitedSpec):
    output_product_image = File(exists=True, desc='average image file')


class MultiplyImages(ANTSCommand):
    """
    Examples
    --------
    >>> from nipype.interfaces.ants import MultiplyImages
    >>> test = MultiplyImages()
    >>> test.inputs.dimension = 3
    >>> test.inputs.first_input = 'moving2.nii'
    >>> test.inputs.second_input = 0.25
    >>> test.inputs.output_product_image = "out.nii"
    >>> test.cmdline # doctest: +ALLOW_UNICODE
    'MultiplyImages 3 moving2.nii 0.25 out.nii'
    """
    _cmd = 'MultiplyImages'
    input_spec = MultiplyImagesInputSpec
    output_spec = MultiplyImagesOutputSpec

    def _format_arg(self, opt, spec, val):
        return super(MultiplyImages, self)._format_arg(opt, spec, val)

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['output_product_image'] = os.path.abspath(
            self.inputs.output_product_image)
        return outputs

class CreateJacobianDeterminantImageInputSpec(ANTSCommandInputSpec):
    imageDimension = traits.Enum(3, 2, argstr='%d', usedefault=False, mandatory=True,
                            position=0, desc='image dimension (2 or 3)')
    deformationField = File(argstr='%s', exists=True, mandatory=True,
                     position=1, desc='deformation transformation file')
    outputImage = File(argstr='%s', mandatory=True,
                         position=2,
                         desc='output filename')
    doLogJacobian = traits.Enum(0, 1, argstr='%d', position=3,
                          desc='return the log jacobian')
    useGeometric = traits.Enum(0, 1, argstr='%d', position=4,
                          desc='return the geometric jacobian')

class CreateJacobianDeterminantImageOutputSpec(TraitedSpec):
    jacobian_image = File(exists=True, desc='jacobian image')

class CreateJacobianDeterminantImage(ANTSCommand):
    """
    Examples
    --------
    >>> from nipype.interfaces.ants import CreateJacobianDeterminantImage
    >>> jacobian = CreateJacobianDeterminantImage()
    >>> jacobian.inputs.imageDimension = 3
    >>> jacobian.inputs.deformationField = 'ants_Warp.nii.gz'
    >>> jacobian.inputs.outputImage = 'out_name.nii.gz'
    >>> jacobian.cmdline # doctest: +ALLOW_UNICODE
    'CreateJacobianDeterminantImage 3 ants_Warp.nii.gz out_name.nii.gz'
    """

    _cmd = 'CreateJacobianDeterminantImage'
    input_spec = CreateJacobianDeterminantImageInputSpec
    output_spec = CreateJacobianDeterminantImageOutputSpec

    def _format_arg(self, opt, spec, val):
        return super(CreateJacobianDeterminantImage, self)._format_arg(opt, spec, val)

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['jacobian_image'] = os.path.abspath(
            self.inputs.outputImage)
        return outputs
