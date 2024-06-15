STATES = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
]

MALE = 'Male'
FEMALE = 'Female'
MIXED = 'Mixed'
COED = 'Coed'
OTHER = 'Other'

GENDER_CHOICES = [
    (MALE, MALE),
    (FEMALE, FEMALE),
    (OTHER, OTHER),
]

TEAM_GENDER_CHOICES = [
    (MALE, MALE),
    (FEMALE, FEMALE),
    (MIXED, MIXED),
    (COED, COED),
]

MILES = 'mi'
KILOMETERS = 'km'
METERS = 'm'

UNIT_CHOICES_CONSTANT = [
    (MILES, 'Miles'),
    (KILOMETERS, 'Kilometers'),
    (METERS, 'Meters'),
]

AM = 'AM'
PM = 'PM'
TIME_INDICATORS = [
    (AM, 'AM'),
    (PM, 'PM'),
]

HOURS = [(i, str(i)) for i in range(1, 13)]
MINUTES = [(i, f'{i:02d}') for i in range(0, 60)]