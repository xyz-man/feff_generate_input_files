'''
* Modified for python3 by Zhenia Syryanyy (Yevgen Syryanyy)
* e-mail: yuginboy@gmail.com
* Last modified: 08.09.2020
'''
"""
A perl Data.Dumper clone for Python
Author: simon@log4think.com
2011-07-08

Copyright 2011 Jinyu LIU

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit 
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions 
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE 
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR 
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
try:
  from types import InstanceType
except ImportError:
  InstanceType = object

def DEBUG(msg, level=None):
    pass


magin_space = '    '
break_base = False
break_string = False

break_before_list_item = True
break_before_list_begin = False
break_after_list_begin = False
break_before_list_end = True
break_after_list_end = False

break_before_tuple_item = True
break_before_tuple_begin = False
break_after_tuple_begin = False
break_before_tuple_end = True
break_after_tuple_end = False

break_before_dict_key = True
break_before_dict_value = False
break_before_dict_begin = False
break_after_dict_begin = False
break_before_dict_end = True
break_after_dict_end = False

DICT_TYPES = {dict: 1}


def atomic_type(t):
    # return t in (NoneType, StringType, IntType, LongType, FloatType, ComplexType)
    return t in (type(None), str, int, float, complex)
    # for val in (type(None), str, int, float, complex):
    #     if isinstance(t, val):
    #         return True
    # return False


def simple_value(val):
    t = type(val)

    if atomic_type(val):
        return True

    # if (t not in DICT_TYPES and t not in (ListType, TupleType) and
    if (t not in DICT_TYPES and t not in (list, tuple) and
            not is_instance(val)):
        return True

    elif t in (list, tuple) and len(val) <= 10:
    # elif t in (ListType, TupleType) and len(val) <= 10:
        for x in val:
            if not atomic_type(type(x)):
                return False
        return True

    elif t in DICT_TYPES and len(val) <= 5:
        for (k, v) in list(val.items()):
            if not (atomic_type(type(k)) and atomic_type(type(v))):
                return False
        return True

    else:
        return False


def is_instance(val):
    # if type(val) is InstanceType:
    if type(val) is object:
        return True
    # instance of extension class, but not an actual extension class
    elif (hasattr(val, '__class__') and
          hasattr(val, '__dict__') and
          not hasattr(val, '__bases__')):
        return True
    else:
        return False


def is_class(val):
    return hasattr(val, '__bases__')


def indent(level=0, nextline=True):
    if nextline:
        return "\n" + magin_space * level
    else:
        return ""


class Dumper:
    def __init__(self, max_depth=999):
        self.max_depth = max_depth
        self.seen = {}

    def reset(self):
        self.seen = {}

    def dump_default(self, obj, level=0, nextline=True):
        DEBUG('; dump_default')
        if level + 1 > self.max_depth:
            return " <%s...>" % type(obj).__class__
        else:
            result = "%s::%s <<" % (type(obj).__name__, obj.__class__)
            if hasattr(obj, '__dict__'):
                result = "%s%s__dict__ :: %s" % (
                    result,
                    indent(level + 1),
                    self.dump_dict(obj.__dict__, level + 1)
                )

            if isinstance(obj, dict):
                result = "%s%sas_dict :: %s" % (
                    result,
                    indent(level + 1),
                    self.dump_dict(obj, level + 1)
                )
            elif isinstance(obj, list):
                result = "%s%sas_list :: %s" % (
                    result,
                    indent(level + 1),
                    self.dump_list(obj, level + 1)
                )

            result = result = "%s%s>>" % (result, indent(level))

        return result

    def dump_base(self, obj, level=0, nextline=True):
        DEBUG("; dump_%s", type(obj).__name__)
        return "%s%s" % (indent(level, break_base), obj)

    dump_NoneType = dump_base
    dump_int = dump_base
    dump_long = dump_base
    dump_float = dump_base

    def dump_str(self, obj, level=0, nextline=True):
        DEBUG('; dump_str')
        return "%s'%s'" % (indent(level, break_string), obj)

    def dump_tuple(self, obj, level=0, nextline=True):
        DEBUG('; dump_tuple')
        if level + 1 > self.max_depth:
            return "%s(...)%s" % (
                indent(level, break_before_tuple_begin),
                indent(level, break_after_tuple_end)
            )
        else:
            items = ["%s%s" % (
                indent(level + 1, break_before_tuple_item),
                self.dump(x, level + 1)
            ) for x in obj
                     ]
            return "%s(%s%s%s)%s" % (
                indent(level, nextline and break_before_tuple_begin),
                indent(level + 1, break_after_tuple_begin), ' '.join(items),
                indent(level, break_before_tuple_end),
                indent(level, break_after_tuple_end)
            )

    def dump_list(self, obj, level=0, nextline=True):
        DEBUG('; dump_list')
        if level + 1 > self.max_depth:
            return "%s[...]%s" % (
                indent(level, break_before_list_begin),
                indent(level, break_after_list_end)
            )
        else:
            items = ["%s%s" % (
                indent(level + 1, break_before_list_item),
                self.dump(x, level + 1)
            ) for x in obj
                     ]
            return "%s[%s%s%s]%s" % (
                indent(level, nextline and break_before_list_begin),
                indent(level + 1, break_after_list_begin), ' '.join(items),
                indent(level, break_before_list_end),
                indent(level, break_after_list_end)
            )

    def dump_dict(self, obj, level=0, nextline=True):
        DEBUG('; dump_dict')
        if level + 1 > self.max_depth:
            return "%s{...}%s" % (
                indent(level, break_before_dict_begin),
                indent(level, break_after_dict_end)
            )
        else:
            items = ["%s%s: %s%s" % (
                indent(level + 1, break_before_dict_key),
                self.dump(k, level + 1),
                indent(level + 2, break_before_dict_value),
                self.dump(v, level + 1)
            ) for k, v in list(obj.items())
                     ]
            return "%s{%s%s%s}%s" % (
                indent(level, nextline and break_before_dict_begin),
                indent(level + 1, break_after_dict_begin), ' '.join(items),
                indent(level, break_before_dict_end),
                indent(level, break_after_dict_end)
            )

    def dump(self, obj, level=0, nextline=True):
        DEBUG('; dump')
        if not simple_value(obj):
            if id(obj) in self.seen:
                return "%s::%s <<...>>" % (type(obj).__name__, obj.__class__)
            else:
                self.seen[id(obj)] = 1

        name = type(obj).__name__
        dump_func = getattr(self, "dump_%s" % name, self.dump_default)
        return dump_func(obj, level, nextline)


def dump(obj, max_depth=999):
    d = Dumper(max_depth)
    return d.dump(obj)


if __name__ == '__main__':
    l1 = [3, 5, 'hello']
    t1 = ('uh', 'oh')
    l2 = ['foo', t1]
    d1 = {'k1': 'val1',
          'k2': l1,
          'k2': l2}

    print()
    print(dump(l1))
    print()
    print(dump(t1))
    print()
    print(dump(l2))
    print()
    print(dump(d1))

    dumper = Dumper(max_depth=1)
    l = {'author': 'joe',
         'created': '03/28/2009',
         'title': 'Yet another blog post',
         'text': 'Here is the text...',
         'tags': ['example', 'joe'],
         'comments': [{'author': 'jim', 'comment': 'I disagree'},
                      {'author': 'nancy', 'comment': 'Good post'}
                      ],
         }
    print()
    print(dumper.dump(l))

    dumper.reset()
    dumper.max_depth = 2
    print()
    print(dumper.dump(l))

    dumper.reset()
    dumper.max_depth = None
    print("max_depth: %s" % dumper.max_depth)


    class Foo(list): pass


    class Bar(dict): pass


    f = Foo()
    b = Bar()

    f.a1 = 35
    f.a2 = l1
    f.a3 = 'foo'
    f.b = b
    f.a4 = l2
    b.a1 = f
    b.a2 = None
    b.a3 = 'bar'

    print()
    print(dump(f))

    print()
    print(dump(Dumper()))

