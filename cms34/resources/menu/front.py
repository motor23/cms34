class Menu(object):

    def __init__(self, env, model):
        self.env = env
        self.model = model

    def get_items(self, **kwargs):
        return self.env.cached_db.query(self.model).filter_by(**kwargs).all()

    def get_item(self, **kwargs):
        items = self.get_items(**kwargs)
        return items and items[0] or None

    def get_menu(self, item=None):
        parent_id = item and item.parent_id or None
        return self.get_items(parent_id=parent_id)

    def get_child_menu(self, item):
        return self.get_items(parent_id=item.id)

    def get_parent(self, item):
        return self.get_item(id=item.parent_id)

    def url_for_item(self, item):
        if not item.section_id:
            child_menu = self.get_child_menu(item)
            if child_menu:
                return self.url_for_item(child_menu[0])
            else:
                return self.env.root.index
        section_list = self.env.sections.get_sections(id=item.section_id)
        if not section_list:
            return self.env.root.index
        return self.env.sections.url_for_section(self.env.root, section_list[0])

    def _get_menus(self, item=None):
        menu = self.get_menu(item)
        if item and item.parent_id:
            parent_item = self.get_item(id=item.parent_id)
            if parent_item:
                return self._get_menus(parent_item) + [(item, menu)]
        return [(item, menu)]

    def get_menus(self, item=None):
        menus = self._get_menus(item)
        if item:
            menus+=[(None, self.get_child_menu(item))]
        return menus


