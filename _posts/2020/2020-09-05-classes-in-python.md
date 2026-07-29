---
layout: post
title: Learning Classes in Python
date: 2020-09-05 21:00
tag:
type: blog
---

I am currently learning python having used a few scripts in some Github Actions to automated some processes using the free serverless compute offered by GitHub.

Having got a few scripts up and running I now want to progress a little more and learn some OOP.

so lets create a class and call it `Polygon` [see line 3] to instantiate the class we need to use a double under notation (known as dunder).
Lets give our shapes some attributes: size, length etc. [see line 4] Note the use of self as the first item in the brackets.

In the below snippet we have assigned variables and done some geometry.

Next we will create a method called `draw` [see line 13]

Note the use of turtle here, which is a package, that can be used for drawing items. At the top of the file we'll include the package

And that's our class, before we get in to running some code to actually draw our shapes, lets make the `Polygon` class a super class and inherit it from a specific shape `Square`

Notice the polygon in brackets and the use of `super()` which essentially says initiate the parent class [see line 24]. We pass in the `4` and the name `square` the rest of the values are the default values from within the super class.

We add to the `square` class [see line 28] another method to draw, which inherits from the super class too, this could be altered in the future, without impacting other shapes.

So to draw a polygon and a square we can use the following snippet

```python
import turtle

class Polygon:
    def __init__(self, sides, name, size=100, color="blue", line_thickness=4):
        self.sides = sides
        self.name = name
        self.size = size
        self.color = color
        self.line_thickness = line_thickness
        self.interior_angles = (self.sides - 2)*180
        self.angle = self.interior_angles/self.sides

    def draw(self):
        turtle.begin_fill()
        turtle.color(self.color)
        turtle.pensize(self.line_thickness)
        for i in range(self.sides):
            turtle.forward(self.size)
            turtle.right(180 - self.angle)
        turtle.end_fill()


class Square(Polygon):
    def __init__(self):
        super().__init__(4, "square")


class Square(Polygon):
    def __init__(self):
        super().__init__(4, "square")

    def draw(self):
        super().draw()


shape = Polygon(6, "hexagon", color="pink")
shape.draw()
turtle.done()

square = Square()
square.draw()
turtle.done()
```

The `turtle.done()` call on line 38 keeps the drawn item on screen like how `console.read()` would do the same in C#.

Square doesn't need any attributes passed in so works just fine with the defaults in its class and the parent class.

Shape, is given 6 sides and named hexagon and has an override of the default colour.

That is Python Classes in a square shaped nutshell
