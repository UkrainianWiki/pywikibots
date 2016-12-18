'''
Напівавтоматизоване виправлення шаблонів {{не перекладено}} які PavloChemBot не забирає бо там перенаправлення.
'''

import re

import pywikibot
from pywikibot import pagegenerators

LIST_PAGE_NAME = 'Користувач:PavloChemBot/Сторінки з невірно використаним шаблоном "Не перекладено"'
REDIRECT_PATTERN = re.compile(r'Page \[\[([^\]]+)\]\] redirects to \[\[([^\]]+)\]\]')

NP_PATTERN = r'\{\{([Нн]е перекладено|[нН]п|[iI]w)\|%s\|(.*?)\|[a-z]*?(\|.+?)?\}\}'
def main():
    find_redirects()

def find_redirects():
    problem_list = pywikibot.Page(pywikibot.Site(), LIST_PAGE_NAME).text.splitlines()
    for line in problem_list:
        test = REDIRECT_PATTERN.findall(line)
        if not test: continue
        s, d = test[0]
        print('\n' * 5, '=' * 80)
        print(s, '->', d)
        for page in pagegenerators.SearchPageGenerator(
            'insource:/\|%s\|/' % s,
            namespaces=[
                0, # Головний/Статті
                1, # Обговорення
                2, # Користувач
                4, # Вікіпедія
                6, # Файл
                10, # Шаблон
                11, # Обговорення шаблону
                12, # Довідка
                13, # Обговорення довідки
                14, # Категорія
                15, # Обговорення категорії
            ]
        ):
            print('\n' * 3, '-' * 80)
            print(page.title())
            for l in page.text.splitlines():
                if s in l:
                    print(l)
            print()
            def r(match): 
                g = match.groups()
                return '[[%s|%s]]' % (d, g[1]) if g[1] else '[[%s]]' % d

            new_text = re.sub(NP_PATTERN % s, r, page.text)
            new_text = re.sub(r'\[\[(.+?)\|\1\]\]', r'[[\1]]', new_text)

            update_page(page, new_text, 'напівавтоматичне прибирання зайвих шаблонів про переклад')

def update_page(page, new_text, description, yes=False):
        if new_text == page.text:
            print('Нічого не міняли')
            return

        pywikibot.showDiff(page.text, new_text)

        print(description)

        if yes or confirmed('Робимо заміну?'):
            page.text = new_text
            page.save(description)

def confirmed(question):
    return pywikibot.input_choice(
        question,
        [('Yes', 'y'), ('No', 'n')],
        default='N'
    ) == 'y'

if __name__ == '__main__':
    main()
