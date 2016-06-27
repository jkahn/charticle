"""Venn diagrams with labeled regions."""
import attr
import matplotlib.pyplot as plt
import matplotlib_venn

from charticle import _validators


@attr.s(slots=True)
class Venn3(object):
    """Object for a 3-label venn.  Set attributes at init or by assignment.

    a_name, b_name, c_name:  Label text for the outer circles.

    a, b, c: Label text for the 1-member patches.

    ab, ac, bc: Label text for the 2-set-intersection patches.

    abc: Label text for the full 3-set intersection.

    title: Text for the title of the plot.

    >>> v3 = Venn3(a_name="useful", b_name = "structured", c_name="delimited")
    >>> v3.abc = "discipline"
    >>> v3.title = "Knowledge"
    >>> v3.fontsizes.title = 22
    >>> v3.sizes.abc *= 3
    >>> v3.plot(); plt.show()
    """

    @attr.s(repr_ns="Venn3", slots=True)
    class Sizes(object):
        """Utility class for shaping the Venn3."""
        a, b, c, ab, ac, bc, abc, normalize = [
            attr.ib(default=1.0, validator=_validators.non_negative)
            for _ in range(8)]

        def set_double_weight(self, weight):
            self.bc = self.ac = self.ab = weight
            return self

        def set_single_weight(self, weight):
            self.a = self.b = self.c = weight
            return self

        def to_dict(self):
            return {
                '100': self.a, '010': self.b, '001': self.c,
                '011': self.bc, '101': self.ac, '110': self.ab,
                '111': self.abc
            }

    @attr.s(repr_ns="Venn3", slots=True)
    class Palette(object):
        """Container of color palette for all 3 items."""
        a, b, c = [attr.ib(default=n, validator=_validators.is_string)
                   for n in ('red', 'green', 'blue')]
        alpha = attr.ib(default=0.4, validator=_validators.zero_to_one)

    @attr.s(repr_ns="Venn3", slots=True)
    class FontSizes(object):
        """Utility class for font size tracking."""
        title = attr.ib(default=20, validator=_validators.positive_int)
        sets = attr.ib(default=14, validator=_validators.positive_int)
        intersections = attr.ib(default=12, validator=_validators.positive_int)

    a_name, b_name, c_name = [attr.ib(default=n,
                                      validator=_validators.is_string)
                              for n in ('A', 'B', 'C')]
    a, b, c = [attr.ib(default=None, validator=_validators.optional_string)
               for n in ('a', 'b', 'c')]
    ab, bc, ac = [attr.ib(default=None, validator=_validators.optional_string)
                  for n in ('a & b', 'b & c', 'a & c')]
    abc = attr.ib(default=None,
                  validator=_validators.optional_string)
    title = attr.ib(default=None, validator=_validators.optional_string)

    sizes = attr.ib(default=attr.Factory(Sizes))
    fontsizes = attr.ib(default=attr.Factory(FontSizes))
    palette = attr.ib(default=attr.Factory(Palette))

    def plot(self, ax=None):
        """Produce a plot on the specified axes.

        Puts label strings in the right places and produces the figure.

        palette: tuple of three color names for sets

        ax: the axis on which to plot this diagram. Defaults to current axes.
        """
        if ax is None:
            ax = plt.axes()

        attr.validate(self)
        attr.validate(self.sizes)
        attr.validate(self.palette)
        attr.validate(self.fontsizes)
        # Adjust the relative size of the areas so that there is more
        # space in the outer ones.
        v = matplotlib_venn.venn3(
            # region sizes,
            subsets=self.sizes.to_dict(), normalize_to=self.sizes.normalize,
            # region colors,
            set_colors=(self.palette.a, self.palette.b, self.palette.c),
            alpha=self.palette.alpha,
            # outer set names
            set_labels=(self.a_name, self.b_name, self.c_name),
            ax=ax)

        # String 'A', 'B', 'C', are the outer set label names declared
        # by matplotlib_venn.
        for label in ('A', 'B', 'C'):
            v.get_label_by_id(label).set_fontsize(self.fontsizes.sets)

        # Numeric strings are the labels for the intersecting regions
        # declared by matplotlib_venn
        for label, val in (
                ('100', self.a), ('010', self.b), ('001', self.c),
                ('110', self.ab), ('011', self.bc), ('101', self.ac),
                ('111', self.abc)):
            t = v.get_label_by_id(label)
            t.set_text("" if val is None else val)
            t.set_fontsize(self.fontsizes.intersections)

        if self.title:
            ax.set_title(self.title, size=self.fontsizes.title)

        return v
