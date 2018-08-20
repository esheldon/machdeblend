import galsim
import numpy as np

class ImageMaker(dict):
    """
    simple image maker
    """
    def __init__(self, config, rng=None):
        self.update(config)

        if rng is None:
            rng=np.random.RandomState()
        self.rng=rng

    def get_scene(self):
        """
        get a scene with multiple objects
        """
        c=self['scene']
        dims = [int(c['size']/self['pixel_scale'])]*2

        halfsize = c['size']/2.0

        offset_radius = halfsize - 0.25*halfsize
        objs=[]
        for i in range(c['nobjects']):
            obj = self._get_object()
            dx, dy = self.rng.uniform(
                low  = -offset_radius,
                high =  offset_radius,
                size=2,
            )
            obj = obj.shift(dx=dx, dy=dy)
            objs.append(obj)

        all_obj = galsim.Sum(objs)
        im = self._get_image(all_obj,dims=dims)
        return im

    def get_one(self):
        """
        get the image for a single object
        """

        obj = self._get_object()
        dx, dy = self._get_pixel_shift()
        obj = obj.shift(dx=dx, dy=dy)

        im = self._get_image(obj)

        return im

    def _get_image(self, obj, dims=None):
        """
        draw the image
        """
        if dims is not None:
            ny,nx = dims
        else:
            ny,nx=None,None,

        im = obj.drawImage(
            nx=nx,
            ny=ny,
            scale=self['pixel_scale'],
        ).array

        self._add_noise(im)

        return im

    def _add_noise(self, im):
        """
        add noise in place
        """
        nim = self.rng.normal(
            scale=self['noise'],
            size=im.shape,
        )
        im += nim

    def _get_pixel_shift(self):
        """
        shifts within one pixel
        """
        dx, dy = self.rng.uniform(
            low  = -0.5*self['pixel_scale'],
            high =  0.5*self['pixel_scale'],
            size=2,
        )
        return dx, dy

    def _get_object(self):
        """
        get one object, without any shifts
        """
        flux=self._get_flux()
        r50=self._get_r50()
        g1,g2 = self._get_shape()

        return galsim.Gaussian(
            flux=flux,
            half_light_radius=r50,
        ).shear(g1=g1,g2=g2)


    def _get_flux(self):
        c=self['objects']['flux']
        assert c['type']=='uniform'
        return self.rng.uniform(
            low=c['range'][0],
            high=c['range'][1],
        )

    def _get_r50(self):
        c=self['objects']['r50']
        assert c['type']=='uniform'
        return self.rng.uniform(
            low=c['range'][0],
            high=c['range'][1],
        )


    def _get_shape(self):
        c=self['objects']['g']
        assert c['type']=='truncated-gaussian'

        while True:
            g1,g2 = self.rng.normal(
                scale=c['sigma'],
                size=2,
            )
            g=np.sqrt(g1**2 + g2**2)
            if g < 0.999:
                break
        return g1,g2

