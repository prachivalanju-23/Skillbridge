from django.core.management.base import BaseCommand
from aptitude.models import Question

# (category, text, options, correct_index, explanation)
DATA = [
    # ---------- Technical ----------
    ('Technical', 'What is the output of console.log(2 + "2");', ['4', '22', 'Error', 'undefined'], 1, 'The number 2 is converted to a string, so + joins them.'),
    ('Technical', 'Which HTML tag is used to create a hyperlink?', ['<a>', '<link>', '<href>', '<url>'], 0, 'The <a> (anchor) tag creates hyperlinks.'),
    ('Technical', 'Which hook is used to manage state in a React function component?', ['useEffect', 'useRef', 'useMemo', 'useState'], 3, 'useState lets a function component hold state.'),
    ('Technical', 'Which of these is a Python web framework?', ['Express', 'React', 'Django', 'Laravel'], 2, 'Django is a Python web framework.'),
    ('Technical', 'Which HTTP method is normally used to create a new resource?', ['GET', 'DELETE', 'HEAD', 'POST'], 3, 'POST is used to create new data on the server.'),
    ('Technical', 'What does typeof null return in JavaScript?', ['object', 'null', 'undefined', 'number'], 0, 'This is a well-known quirk: typeof null is "object".'),
    ('Technical', 'Which CSS property changes the color of text?', ['font-color', 'text-style', 'color', 'foreground'], 2, 'The color property sets the text color.'),
    ('Technical', 'Which of these is NOT a JavaScript data type?', ['String', 'Boolean', 'Float', 'Symbol'], 2, 'JavaScript has Number, not a separate Float type.'),
    ('Technical', 'What does npm stand for?', ['Node Package Manager', 'New Program Module', 'Node Primary Module', 'Network Package Manager'], 0, 'npm is the Node Package Manager.'),
    ('Technical', 'Which keyword declares a block-scoped constant in JavaScript?', ['var', 'let', 'const', 'static'], 2, 'const declares a constant that cannot be reassigned.'),
    ('Technical', 'Which HTTP status code means "Not Found"?', ['200', '404', '500', '301'], 1, '404 means the requested resource was not found.'),
    ('Technical', 'Which SQL command is used to retrieve data from a table?', ['FETCH', 'OPEN', 'GET', 'SELECT'], 3, 'SELECT retrieves rows from a table.'),
    ('Technical', 'Which command applies Django migrations to the database?', ['python manage.py migrate', 'python manage.py runserver', 'python manage.py startapp', 'python manage.py shell'], 0, 'migrate applies the migrations to the database.'),
    ('Technical', 'What does CSS stand for?', ['Computer Style Sheets', 'Creative Style System', 'Cascading Style Sheets', 'Colorful Style Sheets'], 2, 'CSS stands for Cascading Style Sheets.'),
    ('Technical', 'Which Git command creates a new branch and switches to it?', ['git checkout -b name', 'git merge name', 'git push name', 'git clone name'], 0, 'git checkout -b creates and switches to a new branch.'),

    # ---------- Logical ----------
    ('Logical', 'Find the next number: 2, 4, 8, 16, ?', ['24', '30', '64', '32'], 3, 'Each number is doubled.'),
    ('Logical', 'Find the next number: 3, 6, 9, 12, ?', ['15', '14', '16', '18'], 0, 'Each number increases by 3.'),
    ('Logical', 'If all roses are flowers and some flowers fade quickly, which statement must be true?', ['All roses fade quickly', 'No rose fades', 'Some roses are flowers', 'All flowers are roses'], 2, 'All roses are flowers, so some roses are definitely flowers.'),
    ('Logical', 'Which one is the odd one out: Apple, Mango, Banana, Carrot?', ['Apple', 'Mango', 'Banana', 'Carrot'], 3, 'Carrot is a vegetable; the others are fruits.'),
    ('Logical', 'If A = 1, B = 2, C = 3, what is the value of CAB?', ['312', '321', '123', '132'], 0, 'C = 3, A = 1, B = 2, so CAB = 312.'),
    ('Logical', 'Find the next number: 5, 10, 20, 40, ?', ['50', '60', '80', '100'], 2, 'Each number is doubled.'),
    ('Logical', 'Find the next number: 1, 4, 9, 16, ?', ['20', '25', '24', '36'], 1, 'These are square numbers: 5 x 5 = 25.'),
    ('Logical', 'If today is Monday, what day will it be after 10 days?', ['Wednesday', 'Friday', 'Saturday', 'Thursday'], 3, '10 days = 1 week + 3 days, so Monday + 3 = Thursday.'),
    ('Logical', 'Which one is the odd one out: Cube, Circle, Triangle, Square?', ['Cube', 'Circle', 'Triangle', 'Square'], 0, 'A cube is 3-dimensional; the others are flat shapes.'),
    ('Logical', 'Find the next letter: A, C, E, G, ?', ['H', 'I', 'J', 'K'], 1, 'Letters skip one each time, so after G comes I.'),
    ('Logical', 'Book is to reading as fork is to:', ['Writing', 'Eating', 'Drawing', 'Cooking'], 1, 'A book is used for reading; a fork is used for eating.'),
    ('Logical', 'All cats are animals. All animals need food. Therefore:', ['All animals are cats', 'Some cats need no food', 'All cats need food', 'No cat is an animal'], 2, 'Cats are animals, and all animals need food.'),
    ('Logical', 'Find the next number: 100, 90, 80, 70, ?', ['50', '65', '60', '75'], 2, 'Each number decreases by 10.'),
    ('Logical', 'Find the next number: 2, 6, 12, 20, ?', ['28', '30', '32', '26'], 1, 'The differences are 4, 6, 8, so the next difference is 10.'),
    ('Logical', 'Which is the smallest number?', ['0.5', '0.25', '0.75', '0.05'], 3, '0.05 is less than 0.25, 0.5 and 0.75.'),

    # ---------- Quantitative ----------
    ('Quantitative', 'What is 15% of 200?', ['20', '25', '30', '35'], 2, '200 x 15 / 100 = 30.'),
    ('Quantitative', 'A train travels 120 km in 2 hours. What is its speed?', ['40 km/h', '50 km/h', '70 km/h', '60 km/h'], 3, 'Speed = distance / time = 120 / 2 = 60 km/h.'),
    ('Quantitative', 'What is the average of 10, 20, 30, 40, 50?', ['30', '25', '35', '40'], 0, 'The sum is 150, and 150 / 5 = 30.'),
    ('Quantitative', 'If 5 pens cost Rs 50, how much do 8 pens cost?', ['Rs 70', 'Rs 80', 'Rs 75', 'Rs 85'], 1, 'One pen costs Rs 10, so 8 pens cost Rs 80.'),
    ('Quantitative', 'What is the square root of 144?', ['10', '11', '14', '12'], 3, '12 x 12 = 144.'),
    ('Quantitative', 'What is 25% of 80?', ['20', '25', '15', '30'], 0, '80 / 4 = 20.'),
    ('Quantitative', 'What is 7 x 8?', ['54', '56', '64', '48'], 1, '7 x 8 = 56.'),
    ('Quantitative', 'What is 3/4 expressed as a percentage?', ['65%', '70%', '75%', '80%'], 2, '3 / 4 = 0.75 = 75%.'),
    ('Quantitative', 'What is the simple interest on Rs 1000 at 10% per year for 2 years?', ['Rs 100', 'Rs 150', 'Rs 250', 'Rs 200'], 3, 'SI = 1000 x 10 x 2 / 100 = Rs 200.'),
    ('Quantitative', 'What is the perimeter of a square with side 5 cm?', ['10 cm', '20 cm', '25 cm', '15 cm'], 1, 'Perimeter = 4 x 5 = 20 cm.'),
    ('Quantitative', 'What is the area of a rectangle with length 6 and width 4?', ['20', '10', '24', '28'], 2, 'Area = 6 x 4 = 24.'),
    ('Quantitative', 'Solve for x: 2x + 6 = 14', ['4', '3', '5', '6'], 0, '2x = 8, so x = 4.'),
    ('Quantitative', 'What is the LCM of 4 and 6?', ['12', '24', '10', '8'], 0, 'The smallest number divisible by both 4 and 6 is 12.'),
    ('Quantitative', 'A Rs 500 item has a 20% discount. What is the final price?', ['Rs 380', 'Rs 400', 'Rs 420', 'Rs 450'], 1, '20% of 500 = 100, so the price is Rs 400.'),
    ('Quantitative', 'If 2 : 3 = x : 15, what is x?', ['8', '12', '9', '10'], 3, 'x = 2 x 15 / 3 = 10.'),

    # ---------- Verbal ----------
    ('Verbal', "Choose the synonym of 'Rapid':", ['Slow', 'Weak', 'Quick', 'Calm'], 2, 'Rapid means quick.'),
    ('Verbal', "Choose the antonym of 'Ancient':", ['Old', 'Historic', 'Aged', 'Modern'], 3, 'Modern is the opposite of ancient.'),
    ('Verbal', 'Choose the correct sentence:', ['She goes to school daily.', 'She go to school daily.', 'She going to school daily.', 'She gone to school daily.'], 0, 'With "she", the verb takes -es: goes.'),
    ('Verbal', 'Fill in the blank: He is good ___ mathematics.', ['in', 'at', 'on', 'for'], 1, 'The correct phrase is "good at".'),
    ('Verbal', 'Choose the correctly spelled word:', ['Recieve', 'Receve', 'Receive', 'Receeve'], 2, 'Correct spelling: receive (i before e, except after c).'),
    ('Verbal', "Choose the antonym of 'Brave':", ['Cowardly', 'Bold', 'Fearless', 'Heroic'], 0, 'Cowardly is the opposite of brave.'),
    ('Verbal', "Choose the synonym of 'Happy':", ['Sad', 'Joyful', 'Angry', 'Tired'], 1, 'Joyful means happy.'),
    ('Verbal', "What is the plural of 'child'?", ['Childs', 'Childes', 'Children', 'Childrens'], 2, 'The plural of child is children.'),
    ('Verbal', "What is the past tense of 'go'?", ['Goed', 'Gone', 'Going', 'Went'], 3, 'The past tense of go is went.'),
    ('Verbal', 'Fill in the blank: She has been living here ___ 2015.', ['for', 'since', 'from', 'at'], 1, '"Since" is used with a starting point in time.'),
    ('Verbal', "What does the idiom 'a piece of cake' mean?", ['Very easy', 'A dessert', 'Very difficult', 'Expensive'], 0, 'It means something is very easy.'),
    ('Verbal', 'Fill in the blank: ___ apple a day keeps the doctor away.', ['A', 'The', 'An', 'Some'], 2, 'Use "an" before a vowel sound.'),
    ('Verbal', "Choose the synonym of 'Huge':", ['Tiny', 'Enormous', 'Narrow', 'Light'], 1, 'Enormous means very large.'),
    ('Verbal', 'Identify the noun: "The dog barked loudly."', ['barked', 'loudly', 'The', 'dog'], 3, 'Dog is the noun (a thing or animal).'),
    ('Verbal', 'Fill in the blank: They ___ playing football now.', ['is', 'are', 'am', 'be'], 1, 'The plural subject "they" takes "are".'),
]


class Command(BaseCommand):
    help = 'Load the aptitude question bank (replaces existing questions)'

    def handle(self, *args, **options):
        Question.objects.all().delete()
        Question.objects.bulk_create(
            [
                Question(category=c, text=t, options=o, correct_index=i, explanation=e)
                for c, t, o, i, e in DATA
            ]
        )
        self.stdout.write(self.style.SUCCESS(f'Loaded {len(DATA)} aptitude questions'))