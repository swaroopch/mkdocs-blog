__version__ = '0.1.0'

from mkdocs.plugins import BasePlugin
import os.path
import datetime


class Blog(BasePlugin):
    def parse_url(self, url):
        try:
            pieces = url.split('/')
            year = int(pieces[0])
            month = int(pieces[1])
            return (year, month)
        except ValueError:
            return None
        except IndexError:
            return None

    def on_nav(self, nav, config, files):
        # ordered by time
        ordered = []
        # nested by year and month
        chronological = {}

        for f in files:
            parsed = self.parse_url(f.url)
            if parsed:
                year, month = parsed

                yeartime = datetime.datetime(year, 1, 1)
                monthtime = datetime.datetime(year, month, 1)
                mtime = os.path.getmtime(f.abs_src_path)

                ordered.append((f.page, year, month, mtime))

                if not yeartime in chronological:
                    chronological[yeartime] = {}
                if not monthtime in chronological[yeartime]:
                    chronological[yeartime][monthtime] = {}
                chronological[yeartime][monthtime][mtime] = f.page

        ordered.sort(key=lambda tup: (tup[1], tup[2], tup[3]))

        config['ordered'] = ordered
        config['chronological'] = chronological

        return nav
