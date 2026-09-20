from __future__ import annotations

import json
import sys
from pathlib import Path

import frontmatter

CONTENT = Path(__file__).resolve().parent.parent / "content"

TEXTBOOK_ORDER = [
    "peryshkin",
    "gendenshtein",
    "panebrattsev",
    "myakishev",
    "kasyanov",
    "gendenshtein10",
]

TEXTBOOKS = {
    "peryshkin": {
        "title": "Физика. 7–9 классы",
        "author": "А. В. Перышкин",
        "grades": {7: "7 класс", 8: "8 класс", 9: "9 класс"},
        "sections": {
            "vvedenie": "Введение",
            "stroenie-veshchestva": "Первоначальные сведения о строении вещества",
            "vzaimodejstvie-tel": "Взаимодействие тел",
            "davlenie": "Давление твёрдых тел, жидкостей и газов",
            "rabota-energiya": "Работа и мощность. Энергия",
            "teplovye-yavleniya": "Тепловые явления",
            "elektricheskie-yavleniya": "Электрические явления",
            "elektromagnitnye-yavleniya": "Электромагнитные явления",
            "svetovye-yavleniya": "Световые явления",
            "zakony-vzaimodejstviya": "Законы взаимодействия и движения тел",
            "kolebaniya-volny": "Механические колебания и волны. Звук",
            "elektromagnitnoe-pole": "Электромагнитное поле",
            "atomnoe-yadro": "Строение атома и атомного ядра",
            "vselennaya": "Строение и эволюция Вселенной",
        },
    },
    "myakishev": {
        "title": "Физика. 10–11 классы (базовый и углублённый уровни)",
        "author": (
            "Г. Я. Мякишев, Б. Б. Буховцев, Н. Н. Сотский (10 класс); "
            "В. М. Чаругин (11 класс); под ред. Н. А. Парфентьевой"
        ),
        "grades": {10: "10 класс", 11: "11 класс"},
        "sections": {
            "kinematika": "Кинематика точки и твёрдого тела",
            "zakony-nyutona": "Законы механики Ньютона",
            "sily-v-mehanike": "Силы в механике",
            "zakony-sohraneniya": "Законы сохранения в механике",
            "dinamika-vrashcheniya": "Динамика вращательного движения абсолютно твёрдого тела",
            "ravnovesie": "Равновесие абсолютно твёрдых тел",
            "gidrostatika": "Элементы гидростатики и гидродинамики",
            "osnovy-mkt": "Основы молекулярно-кинетической теории",
            "mkt-gaza": "Молекулярно-кинетическая теория идеального газа",
            "uravnenie-sostoyaniya": "Уравнение состояния идеального газа. Газовые законы",
            "prevrashcheniya-zhidkostej": "Взаимные превращения жидкостей и газов",
            "zhidkosti-tverdye": "Жидкости и твёрдые тела",
            "termodinamika": "Основы термодинамики",
            "elektrostatika": "Электростатика",
            "postoyannyj-tok": "Законы постоянного тока",
            "tok-v-sredah": "Электрический ток в различных средах",
            "magnitnoe-pole": "Магнитное поле",
            "elektromagnitnaya-indukciya": "Электромагнитная индукция",
            "mehanicheskie-kolebaniya": "Механические колебания",
            "elektromagnitnye-kolebaniya": "Электромагнитные колебания",
            "mehanicheskie-volny": "Механические волны",
            "elektromagnitnye-volny": "Электромагнитные волны",
            "svetovye-volny": "Световые волны",
            "teoriya-otnositelnosti": "Элементы теории относительности",
            "izluchenie-spektry": "Излучение и спектры",
            "svetovye-kvanty": "Световые кванты",
            "atomnaya-fizika": "Атомная физика",
            "atomnoe-yadro": "Физика атомного ядра",
            "elementarnye-chasticy": "Элементарные частицы",
            "solnechnaya-sistema": "Солнечная система",
            "solnce-zvezdy": "Солнце и звёзды",
            "stroenie-vselennoj": "Строение Вселенной",
        },
    },
    "gendenshtein": {
        "title": "Физика. 7–9 классы",
        "author": "Л. Э. Генденштейн, А. Б. Кайдалов",
        "grades": {7: "7 класс", 8: "8 класс", 9: "9 класс"},
        "sections": {
            "metodologiya": "Физика и физические методы изучения природы",
            "stroenie": "Строение вещества",
            "dvizhenie": "Движение и взаимодействие тел",
            "davlenie": "Давление. Закон Архимеда и плавание тел",
            "rabota": "Работа и энергия",
            "teplovye": "Тепловые явления",
            "elektromagnitnye": "Электромагнитные явления",
            "opticheskie": "Оптические явления",
            "mehanicheskie": "Механические явления",
            "atomy-zvezdy": "Атомы и звёзды",
        },
    },
    "kasyanov": {
        "title": "Физика. 10–11 классы (углублённый уровень)",
        "author": "В. А. Касьянов",
        "grades": {10: "10 класс", 11: "11 класс"},
        "sections": {
            "vvedenie": "Физика в познании вещества, поля, пространства и времени",
            "kinematika-tochki": "Кинематика материальной точки",
            "dinamika-tochki": "Динамика материальной точки",
            "zakony-sohraneniya": "Законы сохранения",
            "dinamika-periodicheskogo": "Динамика периодического движения",
            "statika": "Статика",
            "relyativistskaya-mehanika": "Релятивистская механика",
            "molekulyarnaya-struktura": "Молекулярная структура вещества",
            "mkt-idealnogo-gaza": "Молекулярно-кинетическая теория идеального газа",
            "termodinamika": "Термодинамика",
            "zhidkost-i-par": "Жидкость и пар",
            "tverdoe-telo": "Твёрдое тело",
            "mehanicheskie-volny": "Механические волны. Акустика",
            "sily-elektromagnitnogo": "Силы электромагнитного взаимодействия неподвижных зарядов",
            "energiya-elektromagnitnogo": "Энергия электромагнитного взаимодействия неподвижных зарядов",
            "postoyannyj-tok": "Постоянный электрический ток",
            "magnitnoe-pole": "Магнитное поле",
            "elektromagnetizm": "Электромагнетизм",
            "cepi-peremennogo-toka": "Цепи переменного тока",
            "izluchenie-priem-voln": "Излучение и приём электромагнитных волн",
            "geometricheskaya-optika": "Геометрическая оптика",
            "volnovaya-optika": "Волновая оптика",
            "kvantovaya-teoriya": "Квантовая теория электромагнитного излучения и вещества",
            "atomnoe-yadro": "Физика атомного ядра",
            "elementarnye-chasticy": "Элементарные частицы",
            "evolyuciya-vselennoj": "Эволюция Вселенной",
        },
    },
    "panebrattsev": {
        "title": "Физика. Инженеры будущего. 7–9 классы (углублённый уровень)",
        "author": (
            "В. В. Белага, Н. И. Воронцова, И. А. Ломаченков, Ю. А. Панебратцев; "
            "под ред. Ю. А. Панебратцева"
        ),
        "grades": {7: "7 класс", 8: "8 класс", 9: "9 класс"},
        "sections": {
            "fizika-i-mir": "Физика и мир, в котором мы живём",
            "stroenie-veshchestva": "Строение вещества",
            "dvizhenie-vzaimodejstvie": "Механическое движение. Взаимодействие. Масса",
            "sily-vokrug-nas": "Силы вокруг нас",
            "davlenie": "Давление твёрдых тел, жидкостей и газов",
            "atmosfera": "Атмосфера и атмосферное давление",
            "arhimed": "Закон Архимеда. Плавание тел",
            "rabota-energiya": "Работа, мощность, энергия",
            "prostye-mehanizmy": "Простые механизмы. «Золотое правило» механики",
            "stroenie-teplovye": "Строение и свойства вещества. Тепловые явления",
            "agregatnye": "Изменения агрегатного состояния вещества",
            "teplovye-dvigateli": "Тепловые двигатели",
            "zaryad-pole": "Электрический заряд. Электрическое поле",
            "tok": "Электрический ток",
            "cepi": "Характеристики электрических цепей",
            "magnitnoe-pole": "Магнитное поле",
            "elektromagnitnye": "Электромагнитные явления",
            "kinematika": "Основы кинематики",
            "dinamika": "Основы динамики",
            "statika": "Основы статики",
            "mehanika-zhidkostej": "Механика жидкостей и газов",
            "zakony-sohraneniya": "Законы сохранения энергии и импульса в механике",
            "mehanicheskie-kolebaniya": "Механические колебания и волны",
            "zvuk": "Звук",
            "elektromagnitnye-kolebaniya": "Электромагнитные колебания и волны",
            "geometricheskaya-optika": "Геометрическая оптика",
            "priroda-sveta": "Электромагнитная природа света",
            "kvanty-atom": "Световые кванты. Строение атома",
            "yadro": "Физика атомного ядра. Ядерные реакции",
            "astronomiya": "Астрономия. Строение Вселенной",
        },
        "parts": {
            7: {"chast-1": "Часть 1", "chast-2": "Часть 2"},
            8: {"chast-1": "Часть 1", "chast-2": "Часть 2"},
            9: {"chast-1": "Часть 1", "chast-2": "Часть 2"},
        },
    },
}


def slug_from_filename(name: str) -> str:
    stem = name[:-3] if name.endswith(".md") else name
    if len(stem) > 3 and stem[2] == "-" and stem[:2].isdigit():
        return stem[3:]
    return stem


def build_sections(sections_root: Path, meta: dict) -> list[dict]:
    section_order = list(meta["sections"].keys())
    section_dirs = [d for d in sections_root.iterdir() if d.is_dir()]
    section_dirs.sort(
        key=lambda d: section_order.index(d.name)
        if d.name in section_order
        else len(section_order)
    )
    sections = []
    for section_dir in section_dirs:
        topics = []
        for topic_file in sorted(section_dir.glob("*.md")):
            post = frontmatter.load(topic_file)
            slug = slug_from_filename(topic_file.name)
            relative = topic_file.relative_to(CONTENT).as_posix()
            topics.append(
                {
                    "id": f"{meta['id']}-{meta['grade_id']}-{slug}",
                    "title": post.metadata["title"],
                    "file": relative,
                }
            )
        if topics:
            sections.append(
                {
                    "id": section_dir.name,
                    "title": meta["sections"].get(section_dir.name, section_dir.name),
                    "topics": topics,
                }
            )
    return sections


def build_textbook(textbook_id: str, meta: dict) -> dict:
    root = CONTENT / textbook_id
    grades = []
    for grade_dir in sorted(root.iterdir()):
        if not grade_dir.is_dir() or not grade_dir.name.isdigit():
            continue
        grade_id = int(grade_dir.name)
        common = {"id": textbook_id, "grade_id": grade_id}
        parts_meta = meta.get("parts", {}).get(grade_id)
        if parts_meta:
            part_dirs = [d for d in grade_dir.iterdir() if d.is_dir()]
            part_order = list(parts_meta.keys())
            part_dirs.sort(
                key=lambda d: part_order.index(d.name)
                if d.name in part_order
                else len(part_order)
            )
            parts = []
            for part_dir in part_dirs:
                sections = build_sections(part_dir, {**meta, **common})
                if sections:
                    parts.append(
                        {
                            "id": part_dir.name,
                            "title": parts_meta.get(part_dir.name, part_dir.name),
                            "sections": sections,
                        }
                    )
            if parts:
                grades.append(
                    {
                        "id": grade_id,
                        "title": meta["grades"].get(grade_id, f"{grade_id} класс"),
                        "parts": parts,
                    }
                )
        else:
            sections = build_sections(grade_dir, {**meta, **common})
            if sections:
                grades.append(
                    {
                        "id": grade_id,
                        "title": meta["grades"].get(grade_id, f"{grade_id} класс"),
                        "sections": sections,
                    }
                )
    return {
        "id": textbook_id,
        "title": meta["title"],
        "author": meta["author"],
        "grades": grades,
    }


def main() -> int:
    textbooks = [
        build_textbook(tid, TEXTBOOKS[tid])
        for tid in TEXTBOOK_ORDER
        if tid in TEXTBOOKS
    ]
    manifest = {"textbooks": textbooks}
    (CONTENT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    total = 0
    for textbook in textbooks:
        for grade in textbook["grades"]:
            groups = grade.get("parts") or [grade]
            for group in groups:
                total += sum(len(section["topics"]) for section in group["sections"])
    print(f"manifest.json: {len(textbooks)} textbooks, {total} topics")
    return 0


if __name__ == "__main__":
    sys.exit(main())
