#!/usr/bin/env python3
"""Initialize the diaper tracker database with schema and default brands."""

import models

DEFAULT_BRANDS = [
    'Pampers Swaddlers',
    'Huggies Little Snugglers',
    'Pampers Baby Dry',
    'Huggies Little Movers',
    'Luvs Platinum Protection',
    'up&up',
    "Member's Mark Premium Baby",
    'Rascals Premium Baby',
    'Hello Bello Premium',
    'Honest Company Clean Conscious',
]


def main():
    print('Initializing database...')
    models.init_db()
    print('Database schema created.')

    print('Adding default brands...')
    for brand in DEFAULT_BRANDS:
        models.add_brand(brand)
        print(f'  + {brand}')

    print(f'\nDone! {len(DEFAULT_BRANDS)} brands added.')
    print(f'Database location: {models.DB_PATH}')


if __name__ == '__main__':
    main()
