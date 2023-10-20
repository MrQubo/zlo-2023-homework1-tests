__all__ = ['correctTests', 'moveOutOfTapeTests']


def testGroup(f):
    from functools import wraps

    class Runner:
        def __init__(self, run, eliminateInputTape):
            self.run = run
            self.eliminateInputTape = eliminateInputTape

        def testCase(self, machine, inp, *test):
            from copy import deepcopy

            res_orig = None
            res_trans = None

            try:
                machine_copy = deepcopy(machine)
                machine_trans = self.eliminateInputTape(machine)
                if machine != machine_copy:
                    assert False, 'eliminateInputTape() modified machine'
                res_trans = self.run(machine_trans, list(inp))[-1]
                res_orig = self.run(machine, list(inp))[-1]
                if res_orig != res_trans:
                    assert False, 'Failed test'
            except:
                print('Test:', *test)
                print('Input:', list(inp))
                print('Original:', res_orig)
                print('Transformed:', res_trans)
                raise

    @wraps(f)
    def tests(*args, **kwargs):
        return f(Runner(*args, **kwargs))

    return tests

@testGroup
def correctTests(self):
    import itertools

    # Palindroms

    machine = { 'initial' : 'p',
              'transitions' : [
               {'state before' : 'p', 'state after' : 'p', 'input letter before' : '⊢','move input head' : 1,'move work head' : 1,'work letter after' : '⊢'},
                  {'state before' : 'p', 'state after' : 'p', 'input letter before' : 'a', 'move input head' : 1, 'move work head' : 1,'work letter after' : 'a'},
                  {'state before' : 'p', 'state after' : 'p', 'input letter before' : 'b', 'move input head' : 1, 'move work head' : 1, 'work letter after' : 'b'},
                  {'state before' : 'p', 'state after' : 'q', 'input letter before' : '⊣', 'move input head' : -1},
                  {'state before' : 'q', 'state after' : 'q', 'input letter before' : 'a','move input head' : -1},
                  {'state before' : 'q', 'state after' : 'q', 'input letter before' : 'b', 'move input head' : -1},
                  {'state before' : 'q', 'state after' : 'r', 'input letter before' : '⊢','move input head' : 1,'move work head' : -1},
                  {'state before' : 'r', 'state after' : 'r', 'input letter before' : 'a','work letter before' : 'a' ,'move work head' : -1, 'move input head' : 1},
                  {'state before' : 'r', 'state after' : 'r', 'input letter before' : 'b','work letter before' : 'b' ,'move work head' : -1, 'move input head' : 1},
                {'state before' : 'r', 'input letter before' : '⊣','halt' : 'accept' },
               ]
              }

    for l in range(6):
        for p in itertools.product('abc', repeat=l):
            self.testCase(machine, p, 'Palindroms', l)

    # Palindroms but with long letters

    machine = { 'initial' : '',
              'transitions' : [
               {'state before' : '', 'state after' : '', 'input letter before' : '⊢','move input head' : 1,'move work head' : 1,'work letter after' : '⊢⊢'},
                  {'state before' : '', 'state after' : '', 'input letter before' : 'aa', 'move input head' : 1, 'move work head' : 1,'work letter after' : 'xx'},
                  {'state before' : '', 'state after' : '', 'input letter before' : 'bb', 'move input head' : 1, 'move work head' : 1, 'work letter after' : 'yy'},
                  {'state before' : '', 'state after' : 'qq', 'input letter before' : '⊣', 'move input head' : -1},
                  {'state before' : 'qq', 'state after' : 'qq', 'input letter before' : 'aa','move input head' : -1},
                  {'state before' : 'qq', 'state after' : 'qq', 'input letter before' : 'bb', 'move input head' : -1},
                  {'state before' : 'qq', 'state after' : 'rr', 'input letter before' : '⊢','move input head' : 1,'move work head' : -1},
                  {'state before' : 'rr', 'state after' : 'rr', 'input letter before' : 'aa','work letter before' : 'xx' ,'move work head' : -1, 'move input head' : 1},
                  {'state before' : 'rr', 'state after' : 'rr', 'input letter before' : 'bb','work letter before' : 'yy' ,'move work head' : -1, 'move input head' : 1},
                {'state before' : 'rr', 'input letter before' : '⊣','halt' : 'accept' },
               ]
              }

    for l in range(4):
        for p in itertools.product(('a', 'b', 'aa', 'bb'), repeat=l):
            self.testCase(machine, p, 'Palindroms ll', l)

    # Machine with no transitions

    machine = {
        'initial': '',
        'transitions': [],
    }
    self.testCase(machine, [], 'Empty')

    # Immediately halting machine

    machine = {
        'initial': '',
        'transitions': [
            { 'state before': '',
              'halt': '' },
        ],
    }
    self.testCase(machine, [], 'Halt')

    machine = {
        'initial': '',
        'transitions': [
            { 'state before': 'xx',
              'halt': '' },
        ],
    }
    self.testCase(machine, [], 'Missing initial')

    # Non-terminating machine

    machine = {
        'initial': '',
        'transitions': [ { 'state before': '', 'state after': '' } ],
    }
    self.testCase(machine, [], 'Endless')

    machine = {
        'initial': '',
        'transitions': [ { 'state before': '', 'state after': '', 'move work head': 1 } ],
    }
    self.testCase(machine, [], 'Endless moving')

    # Check first cell of work tape is '⊢'

    machine = {
        'initial': '',
        'transitions': [
            { 'state before': '', 'work letter before': '⊢',
              'halt': '⊢' },
            { 'state before': '', 'work letter before': '',
              'halt': '' },
        ],
    }

    self.testCase(machine, [], 'First cell')

    # Check second cell of work tape is ''

    machine = {
        'initial': '',
        'transitions': [
            { 'state before': '',
              'state after': 'pp', 'move work head': 1 },
            { 'state before': 'pp', 'work letter before': '⊢',
              'halt': '⊢' },
            { 'state before': 'pp', 'work letter before': '',
              'halt': '' },
        ],
    }

    self.testCase(machine, [], 'Second cell')

    # Test moving input head

    for st in ('qq', 'pp'):
        for ww in ('', '⊣'):
            permuted_transitions = [
                { 'state before': st, 'work letter before': ww, 'input letter before': 'aa',
                  'state after': 'qq', 'move work head': -1, 'move input head': -1 },
                { 'state before': st, 'work letter before': ww, 'input letter before': 'bb',
                  'state after': 'qq', 'move work head': -1, 'move input head': 1 },

                { 'state before': 'qq', 'work letter before': '', 'input letter before': 'bb',
                  'state after': 'qq', 'move work head': -1, 'move input head': -1 },
                { 'state before': 'qq', 'work letter before': '', 'input letter before': 'aa',
                  'state after': 'qq', 'move work head': -1, 'move input head': 1 },
            ]
            for perm_idx, perm in enumerate(itertools.permutations(permuted_transitions)):
                machine = {
                    'initial': '',
                    'transitions': [
                        { 'state before': '',
                          'state after': '0', 'move work head': 1, 'move input head': 1 },
                        { 'state before': '0',
                          'state after': st, 'work letter after': ww, 'move work head': 1, 'move input head': 1 },

                        *perm,

                        { 'state before': 'qq', 'work letter before': '⊢', 'input letter before': 'aa',
                          'halt': 'aa' },
                        { 'state before': 'qq', 'work letter before': '⊢', 'input letter before': 'bb',
                          'halt': 'bb' },
                        { 'state before': 'qq', 'work letter before': '⊢', 'input letter before': '⊢',
                          'halt': '⊢' },
                        { 'state before': 'qq', 'work letter before': '⊢', 'input letter before': '⊣',
                          'halt': '⊣' },
                    ],
                }

                for p in itertools.product(('aa', 'bb'), repeat=3):
                    self.testCase(machine, p, 'Moving input head', st, ww, perm_idx)

    # Test moving work head

    for st in ('qq', 'pp'):
        permuted_transitions = [
            { 'state before': st, 'input letter before': 'aa',
              'state after': 'qq', 'move work head': -1, 'move input head': 1 },
            { 'state before': st, 'input letter before': 'bb',
              'state after': 'qq', 'move work head': 1, 'move input head': 1 },

            { 'state before': 'qq', 'input letter before': 'bb',
              'state after': 'qq', 'move work head': -1, 'move input head': 1 },
            { 'state before': 'qq', 'input letter before': 'aa',
              'state after': 'qq', 'move work head': 1, 'move input head': 1 },
        ]
        for perm_idx, perm in enumerate(itertools.permutations(permuted_transitions)):
            machine = {
                'initial': '0',
                'transitions': [
                    *({ 'state before': str(i),
                        'state after': str(i+1), 'work letter after': str(i), 'move work head': 1 }
                            for i in range(4)),
                    { 'state before': '4',
                      'state after': 'bb', 'work letter after': '4', 'move work head': -1 },
                    { 'state before': 'bb',
                      'state after': st, 'move work head': -1, 'move input head': 1 },

                    *perm,

                    *({ 'state before': 'qq', 'work letter before': str(i), 'input letter before': '⊣',
                        'halt': str(i) }
                            for i in range(5)),
                ],
            }

            for p in itertools.product(('aa', 'bb'), repeat=2):
                self.testCase(machine, p, 'Moving work head', st, perm_idx)

@testGroup
def moveOutOfTapeTests(self):

    # Move out of input tape (left)

    machine = {
        'initial': '',
        'transitions': [
            { 'state before': '',
              'state after': 'qq', 'move input head': -1 },
            { 'state before': 'qq',
              'halt': '' },
        ],
    }

    self.testCase(machine, [], 'OOB input left')

    # Move out of input tape (right)

    for l in range(3):
        for k in range(l-1, l+2):
            machine = {
                'initial': '0',
                'transitions': [
                    *({ 'state before': str(i),
                        'state after': str(i+1), 'move input head': 1 }
                             for i in range(k)),
                    { 'state before': str(k),
                      'halt': '' },
                ],
            }

        self.testCase(machine, ['x' for _ in range(l)], 'OOB input right', l, k)

    # Move out of work tape

    machine = {
        'initial': '',
        'transitions': [
            { 'state before': '',
              'state after': 'qq', 'move work head': -1 },
            { 'state before': 'qq',
              'halt': '' },
        ],
    }

    self.testCase(machine, [], 'OOB work')
