import re
from typing import Dict, List
from bs4 import BeautifulSoup
from bs4.element import Tag


class ParserService:
    def extract_classes_with_dragons_urls(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, "html.parser")
        
        container = soup.select_one("div.mw-content-ltr.mw-parser-output")
        
        if not container: return []

        for ref in container.select("sup.reference"): ref.decompose()

        classes_data, current_class = [], None

        for element in container.find_all(["h2", "figure", "p", "ul"]):
            if element.name == "h2":
                if current_class and current_class.get("name"):
                    classes_data.append(current_class)
                span_node = element.find("span", class_="mw-headline") or element.find("span")
                class_name = span_node.get_text(strip=True) if span_node else element.get_text(strip=True)
                if re.search(r"^.*Class$", class_name):
                    current_class = {"name": class_name,"icon" : None,"description": "","dragons": []}
            
            elif current_class:
                if element.name == "figure":
                    style = element.get("style", "") 
                    if "180px" in style:
                        a_tag = element.find("a", class_="mw-file-description") or element.find("a", href=True)
                        if a_tag: current_class["icon"] = a_tag.get("href")
            
                elif element.name == "p":
                    full_text = element.get_text(strip=True)
                    if "The dragon species included" in full_text:
                        clean_text = full_text.split("The dragon species included")[0].strip()
                        current_class["description"] = clean_text
            
                elif element.name == "ul":
                    for a in element.find_all("a",href=True):
                        href = a["href"]
                        if href.startswith("/wiki/") and not any(x in href for x in [":", "#", "Category"]):
                            dragon_info = {
                                "name": a.get_text(strip=True),
                                "url": f"https://howtotrainyourdragon.fandom.com{href}"
                            }

                            if dragon_info not in current_class["dragons"]:
                                current_class["dragons"].append(dragon_info)
        if current_class and current_class.get("name"): classes_data.append(current_class) 
        
        return classes_data

    def _get_data_value(self, infobox: Tag, data_source: str) -> Tag | None:
        node = infobox.find(attrs={"data-source": data_source})
        if not node:
            return None
        return node.find("div", class_=lambda c: c and "pi-data-value" in c)

    def _get_br_list(self, infobox: Tag, data_source: str) -> list[str]:
        val_div = self._get_data_value(infobox, data_source)
        if not val_div:
            return []
        return [s.strip() for s in val_div.stripped_strings if s.strip()]

    def _parse_int(self, text: str) -> int:
        if not text:
            return 0
        clean_text = text.replace(",", "").replace(".", "")
        match = re.search(r"\d+", clean_text)
        return int(match.group()) if match else 0
    
    def extract_dragons_data(self, html: str) -> Dict:
        soup = BeautifulSoup(html, "html.parser")

        infobox = soup.find(
            "aside", class_=lambda c: c and "portable-infobox" in c
        )

        if not infobox:
            infobox = soup.find(class_=lambda c: c and "portable-infobox" in c)

        if not infobox:
            return {}

        def _get_stat(key: str) -> int:
            node = self._get_data_value(infobox, key)
            return self._parse_int(node.get_text()) if node else 0

        images = []

        for img in infobox.select("img"):
            src = img.get("src")

            if src and src not in images:
                images.append(src)

        abilities_list = self._get_br_list(infobox, "Abilities")
        abilities = [{"name": ab_name} for ab_name in abilities_list]

        distributions = []
        dist_container = self._get_data_value(infobox, "Distribution")
        if dist_container:
            dist_links = dist_container.find_all("a")
            for link in dist_links:
                name = link.get_text(strip=True)
                alt_name = link.get("title", "")
                if name: distributions.append({"name": name, "alternatenames": alt_name,})

        name_node = infobox.find(attrs={"data-source": "Name"})
        species = name_node.get_text(strip=True) if name_node else ""

        fire_type_node = self._get_data_value(infobox, "Fire Type")
        fire_type = (fire_type_node.get_text(strip=True) if fire_type_node else "")

        size_node = self._get_data_value(infobox, "Size")
        size_str = size_node.get_text(strip=True) if size_node else ""

        weight_node = self._get_data_value(infobox, "Weight")
        weight_val = self._parse_int(weight_node.get_text(strip=True) if weight_node else "")

        wingspan_node = self._get_data_value(infobox, "Wingspan")
        wingspan_val = self._parse_int(wingspan_node.get_text(strip=True) if wingspan_node else "")

        trainable_node = self._get_data_value(infobox, "Trainable")
        trainable_val = (trainable_node.get_text(strip=True).lower() == "yes" if trainable_node else False)

        dragon_data = {
            "species": species,
            "firetype": fire_type,
            "features": self._get_br_list(infobox, "Features"),
            "colors": self._get_br_list(infobox, "Colors"),
            "diet": self._get_br_list(infobox, "Food"),
            "habitat": self._get_br_list(infobox, "Habitat"),
            "size": size_str,
            "weight": weight_val,
            "wingspan": wingspan_val,
            "trainable": trainable_val,
            "attack": _get_stat("Attack2"),
            "speed": _get_stat("Speed2"),
            "armor": _get_stat("Armor2"),
            "firepower": _get_stat("Firepower"),
            "shotlimit": _get_stat("Shot Limit2"),
            "venom": _get_stat("Venom2"),
            "jawstrength": _get_stat("Jaw Strength2"),
            "abilities": abilities,
            "distributions": distributions,
            "images": images,
        }

        return dragon_data