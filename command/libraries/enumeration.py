#!/usr/bin/python
#-*-python-*-##################################################################
# Copyright 2017 - 2023 Inesonic, LLC
# 
# This file is licensed under two licenses.
#
# Inesonic Commercial License, Version 1:
#   All rights reserved.  Inesonic, LLC retains all rights to this software,
#   including the right to relicense the software in source or binary formats
#   under different terms.  Unauthorized use under the terms of this license is
#   strictly prohibited.
#
# GNU Public License, Version 3:
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the Free
#   Software Foundation, either version 3 of the License, or (at your option)
#   any later version.
#   
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#   more details.
#   
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <https://www.gnu.org/licenses/>.
###############################################################################

"""
This Python module provides support for type-safe enumerations within Python
programs.  You can create a variable from the Enumeration class indicating what
enumerated values the class instance can take on.  The enumerated values should
be provided as a space separated string of names.

my_enumeration = Enumeration(
    "ENUM_A "
    "ENUM_B "
    "ENUM_C "
)

You can then access each individual enumerated value using an expression of the
form:

if my_enumeration.ENUM_A != current_state:
    ....

If the value of current_state is not a value from my_enumeration then a Python
ValueError exception will be thrown.

This module was inspired by several examples found at:

    http://code.activestate.com/recipes/67107

"""

###############################################################################
# Value class:
#

class Value(object):
    """
    Class that supports individual values in an enumerated type.

    """

    def __init__(self, value, name, parent):
        """
        Initialization method for Value.

        :param value:
            A numerical value to assign to this enumeration.

        :param name:
            The string name to assign to this enumeration.

        :param parent:
            Index of the parent class that owns this enumerated value.

        :type value:  int or long
        :type name:   str
        :type parent: enumeration.Enum

        """

        self.__value  = value
        self.__name   = name
        self.__parent = parent


    def __lt__(self, b):
        """
        Compares this class instance with another instance.  This method
        returns true if this instance should be ordered before b.

        :param b:
            The value being compared against this class.

        :type b: enumeration.Value

        :return:
            Returns true if this instance should precede b.  Returns false if
            this instance equals b or follows b.

        :rtype: bool

        """

        if self.__parent != b.__parent:
            raise ValueError("enumeration values are incompatible")

        return self.__value < b.__value


    def __gt__(self, b):
        """
        Compares this class instance with another instance.  This method
        returns true if this instance should be ordered after b.

        :param b:
            The value being compared against this class.

        :type b: enumeration.Value

        :return:
            Returns true if this instance follows b.  Returns false if this
            instance precedes or is equal to b.

        :rtype: bool

        """

        if self.__parent != b.__parent:
            raise ValueError("enumeration values are incompatible")

        return self.__value > b.__value


    def __le__(self, b):
        """
        Compares this class instance with another instance.  This method
        returns true if this instance should be ordered before or with b.

        :param b:
            The value being compared against this class.

        :type b: enumeration.Value

        :return:
            Returns true if this instance precedes b or is equal to b.  Returns
            false if this follows b.

        :rtype: bool

        """

        if self.__parent != b.__parent:
            raise ValueError("enumeration values are incompatible")

        return self.__value <= b.__value


    def __ge__(self, b):
        """
        Compares this class instance with another instance.  This method
        returns true if this instance should be ordered after or with b.

        :param b:
            The value being compared against this class.

        :type b: enumeration.Value

        :return:
            Returns true if this instance follows b or is equal to b.  Returns
            false if this precedes b.

        :rtype: bool

        """

        if self.__parent != b.__parent:
            raise ValueError("enumeration values are incompatible")

        return self.__value >= b.__value


    def __eq__(self, b):
        """
        Compares this class instance with another instance.  This method
        returns true if this instance is the same as b.

        :param b:
            The value being compared against this class.

        :type b: enumeration.Value

        :return:
            Returns true if this instance is the same as b.

        :rtype: bool

        """

        if self.__parent != b.__parent:
            raise ValueError("enumeration values are incompatible")

        return self.__value == b.__value


    def __ne__(self, b):
        """
        Compares this class instance with another instance.  This method
        returns true if this instance is not the same as b.

        :param b:
            The value being compared against this class.

        :type b: enumeration.Value

        :return:
            Returns true if this instance is not the same as b.

        :rtype: bool

        """

        if self.__parent != b.__parent:
            raise ValueError("enumeration values are incompatible")

        return self.__value != b.__value


    def __hash__(self):
        """
        Returns a unique numeric identifier for the enumerated value.

        :return:
            Returns the numeric value of this class instance.

        :rtype: int or long

        """

        return self.__value


    def __repr__(self):
        """
        Returns a representation of the enumerated value.

        :return:
            Returns a string representation of this class instance.

        :rtype: str

        """

        return "Value(%s,\"%s\",%d)"%(
            self.__value,
            self.__name,
            self.__parent
        )


    def __str__(self):
        """
        Returns the common name of the enumerated value.

        :return:
            Returns a nice representation of this enumeration.

        :rtype: str

        """

        return self.__name


    @property
    def value(self):
        """
        Returns a numeric value that can be used to identify the enumerated
        value.

        :return:
            Returns a unique numeric value associated with this value.

        :rtype: int or long

        """

        return self.__value


    def is_member(self, e):
        """
        Method that determines if this value belongs to a specific enumeration.

        :param e:
            The enumeration to check.

        :type v: enumeration.Enum

        :return:
            Returns True if the value is a member of the enumeration. Returns
            False if the value is not a member of the enumeration.

        """

        if e._index == self.__parent:
            return True
        else:
            return False

###############################################################################
# Enum class:
#

class Enum(list):
    """
    Class that supports type safe enumerated values.  You can access enumerated
    values by one of several ways:

        my_enum = Enum("ENUM_A ENUM_B ENUM_C")

        print(my_enum.ENUM_A) # prints "ENUM_A"
        print(my_enum[0])     # also prints "ENUM_A"


    """

    __next_parent_index = 1


    def __init__(self, values):
        """
        Initialization method for Enum

        values - A space separated list of enumerated values.

        """

        self._index = Enum.__next_parent_index
        Enum.__next_parent_index += 1

        self._values_by_name = dict()
        for n in values.split():
            self.add(n)


    def add(self, name):
        """
        Adds a new value to this enumeration.  The value will only be added if
        it is not currently defined in the enumeration.

        :param name:
            The name of the newly added enumeration.

        :return:
            Returns the newly added enumerated value.

        :type name: str
        :rtype:     Value

        """

        if not name in self._values_by_name:
            v = Value(len(self), name, self._index)
            setattr(self, name, v)
            self.append(v)
            self._values_by_name[name] = v
        else:
            v = self._values_by_name[name]

        return v;


    def by_name(self, s):
        """
        Returns the value associated with the given name.

        :param s:
            The name to locate.

        :type s: str

        :return:
            Returns the enumerated value associated with the given name.  A
            value of None is returned if the name is not assigned to this
            enumerated type.

        :rtype: enumeration.Value or None

        """

        if s in self._values_by_name:
            return self._values_by_name[s]
        else:
            return None


    def by_value(self, i):
        """
        Returns the value associated with the given index.

        :param i:
            The the value associated with this enumeration.

        :type i: int or long

        :return:
            Returns the enumerated value associated with the given name.  A
            value of None is returned if the index is invalid.

        :rtype: enumeration.Value or None

        """

        if i >= 0 and i < len(self):
            return self[i]
        else:
            return None


    def strings(self):
        """
        Returns a list of strings for the enumerated type.

        :return:
            Returns a list of strings for the enumerated type.

        :rtype: list

        """

        return [ str(v) for v in self ]

###############################################################################
# Test code:
#

if __name__ == "__main__":
    e1 = Enum("ENUM_A ENUM_B ENUM_C")
    e2 = Enum("ENUM_D ENUM_E ENUM_F")

    print("Enumerations in e1:")
    for v in e1:
        print("  %s = %d"%(str(v),v.value))

    print("Enumerations in e2:")
    for v in e2:
        print("  %s = %d"%(str(v),v.value))

    print("Checking \"by\" methods...")
    for i in range(len(e1)):
        vi = e1.by_value(i)
        s = str(vi)
        vs = e1.by_name(s)

        if e1[i] != vi:
            print("*** Mismatch by index.")

        if e1[i] != vs:
            print("*** Mismatch by name.")

    print("Checking \"strings\" methods...")
    print("e1: %s"%str(e1.strings()))
    print("e2: %s"%str(e2.strings()))

    print("Comparing enumerations in e1:")

    for v1 in e1:
        for v2 in e1:
            if v1 == v2:
                print("%s == %s"%(str(v1), str(v2)))
            else:
                print("%s != %s"%(str(v1), str(v2)))

    print("Trying to compare enumerations in e1 and e2:")

    for v1 in e1:
        for v2 in e2:
            try:
                if v1 == v2:
                    print("unexpected %s == %s"%(str(v1), str(v2)))
                else:
                    print("unexpected %s != %s"%(str(v1), str(v2)))
            except:
                print("expected   %s == %s2 raises exception."%(
                    str(v1),
                    str(v2)
                ))
