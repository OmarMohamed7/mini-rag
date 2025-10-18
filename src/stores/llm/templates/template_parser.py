import importlib
import os
from string import Template


class TemplateParser:
    def __init__(self, locale: str = "en"):
        self.templates = {}
        self.default_locale = "en"

        self.set_locale(locale)

    def set_locale(self, locale: str):
        path = os.path.join(os.path.dirname(__file__), "locales", locale)
        if locale not in ["en", "ar"]:
            self.default_locale = "en"
        else:
            self.default_locale = locale

        if not self.check_path_exists(path):
            raise ValueError(f"Path not found: {path}")
        else:
            self.templates_dir = path

    def check_path_exists(self, path: str):
        if not os.path.exists(path):
            raise ValueError(f"Path not found: {path}")

        return True

    def get_template(self, template: str, key: str = None, vars: dict = {}):
        template_path = os.path.join(self.templates_dir, f"{template}.py")
        if not os.path.exists(template_path):
            raise ValueError(f"Template not found: {template_path}")

        locale_package = (
            f"stores.llm.templates.locales.{self.default_locale}.{template}"
        )

        module = importlib.import_module(locale_package)

        if not module:
            raise ValueError(f"Module not found: {locale_package}")

        key_attribute: str = getattr(module, key)

        template_obj = None
        if isinstance(key_attribute, Template):
            template_obj = key_attribute
            template_obj = template_obj.substitute(vars)
        elif isinstance(key_attribute, str):
            template_obj = Template(key_attribute)
            template_obj = template_obj.substitute(vars)

        if not template_obj:
            raise ValueError(f"Template not found: {key_attribute}")

        return template_obj
