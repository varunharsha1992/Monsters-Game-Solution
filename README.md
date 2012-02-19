# Monsters Game, a developer test

   The solution of this problem exist in the directory solution.
   A fork hasn't been made to avoid of having the solution too accessible.
   

You are given a map containing the names of cities in the non-existent
world of X.  The map is in a file, with one city per line.  The city
name is first, followed by 1-4 directions (north, south, east, or
west).  Each one represents a road to another city that lies in that
direction.

For example:

    Foo north=Bar west=Baz south=Qu-ux
    Bar south=Foo west=Bee
    ...

The city and each of the pairs are separated by a single space, and
the directions are separated from their respective cities with an
equals (`=`) sign.

In this world you are competing to be the evil overlord, so you create
many monsters to go forth and cause trouble.  You should create `N`
monsters, where `N` is specified as a commandline argument.

These monsters start out at random places on the map, and wander
around randomly, following links.  Each iteration, the monsters can
travel in any of the directions leading out of a city.  In our example
above, a monster that starts at Foo can go north to Bar, west to Baz,
or south to Qu-ux.

When two monsters end up in the same place, they fight, and in the
process kill each other and destroy the city.  When a city is
destroyed, it is removed from the map, and so are any roads that lead
into or out of it.

In our example above, if Bar were destroyed the map would now be
something like:

    Foo west=Baz south=Qu-ux
    ...

Once a city is destroyed, monsters can no longer travel to or through
it.  This may lead to monsters getting "trapped" -- that's ok, you
don't care, because you're an evil overlord.

You should create a program that reads in the world map, creates `N`
monsters, and unleashes them.  The program should run until all the
monsters have been destroyed, or each monster has moved at least
10,000 times.  When two monsters fight, print out a message like:

    Bar has been destroyed by monster 10 and monster 34!

(If you want to give them names, you may, but it is not required.)
Once the program has finished, it should print out whatever is left of
the world in the same format as the input file.

Feel free to make assumptions (for example, that the city names will
never contain numeric characters), but please add comments or
assertions describing the assumptions you are making.


#### Credit

[Playfire](https://www.playfire.com/)
