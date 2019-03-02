import os.path

import bokeh.resources
import bokeh.util.paths


class LocalResource(bokeh.resources.Resources):
    """Allows loading JS and CSS files from a different location.
    """
    def __init__(self, res_dir, mode='relative', version=None, root_dir=None,
                 minified=True, log_level="info", root_url=None,
                 path_versioner=None, components=None):

        super().__init__(mode=mode, version=version, root_dir=root_dir,
                         minified=minified, log_level=log_level,
                         root_url=root_url, path_versioner=path_versioner,
                         components=components)

        if res_dir is not None:
            self.res_dir = res_dir
        else:
            self.res_dir = bokeh.util.paths.bokehjsdir(self.dev)

    def _file_paths(self, kind):
        minified = ".min" if not self.dev and self.minified else ""
        files = ["%s%s.%s" % (component, minified, kind)
                 for component in self.components(kind)]
        paths = [os.path.join(self.res_dir, kind, file) for file in files]
        return paths
