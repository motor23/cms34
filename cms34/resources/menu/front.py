class Menu(object):

    def __init__(self, env, model):
        self.env = env
        self.model = model

    def get_items(self, **kwargs):
        result = []
        _query = self.env.db.query(self.model)
        items = self.env.cached_db.query(self.model, _query)\
                                  .filter_by(**kwargs)\
                                  .order_by('order').all()
        for item in items:
            if item.section_id:
                section = self.env.sections.get_section(id=item.section_id)
                if not section:
                    continue
            result.append(item)
        return result

    def get_item(self, **kwargs):
        items = self.get_items(**kwargs)
        return items and items[0] or None

    def get_menu(self, item=None):
        parent_id = item and item.parent_id or None
        return self.get_items(parent_id=parent_id)

    def get_child_menu(self, item=None):
        return self.get_items(parent_id=item and item.id or None)

    def get_parent(self, item):
        return self.get_item(id=item.parent_id)

    def get_parents(self, item):
        result = []
        parent = self.get_parent(item)
        while parent:
            result.append(parent)
            parent = self.get_parent(parent)
        result.reverse()
        return result

    def url_for_item(self, item):
        if not item.section_id:
            child_item = self.get_item(parent_id=item.id)
            if child_item:
                return self.url_for_item(child_item)
            else:
                return self.env.root.index
        section = self.env.sections.get_section(id=item.section_id)
        if not section:
            return self.env.root.index
        return self.env.sections.url_for_section(self.env.root, section)

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
            child_menu = self.get_child_menu(item)
            if child_menu:
                menus+=[(None, child_menu)]
        return menus

    def get_item_by_section(self, section=None):
        menu_item = None
        if section:
            menu_item = self.get_item(section_id=section.id)
            while not menu_item and section.parent_id:
                section = self.env.sections.get_section(id=section.parent_id)
                menu_item = self.get_item(section_id=section.id)
        return menu_item

    def get_menus_by_section(self, section=None):
        return self.get_menus(self.get_item_by_section(section))

    def get_menu_tree(self, level=1, selected_item=None, item=None):
        if selected_item:
            selected_items = self.get_parents(selected_item) + [selected_item]
        else:
            selected_items = []
        return self._get_menu_tree(level, selected_items, item)

    def _get_menu_tree(self, level=1, selected_items=None, item=None):
        if selected_items is None:
            selected_items = []
        result = []
        if level:
            for subitem in self.get_child_menu(item):
                submenu = self._get_menu_tree(level-1, selected_items, subitem)
                # Sometimes multiple menu items can point to the same place
                if any(item for item in selected_items
                       if subitem.section_id == item.section_id):
                    selected_items.append(subitem)
                selected = subitem in selected_items
                result.append((subitem, selected, submenu))
        return result


