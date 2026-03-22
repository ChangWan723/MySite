---
title: "Visitor Pattern: the Design Pattern Born from the Defect"
date: 2024-10-05 09:01:00 UTC
categories: [(CS) Learning Note, OOP]
tags: [software engineering, OOP, Design Patterns, Design Principles]
pin: false
image:
  path: /assets/img/posts/VisitorPattern.jpg
---

The Visitor Pattern is one of the most complex design patterns, and the code that uses this pattern is often difficult to understand. In that blog, I will go over the Visitor Pattern, which will allow you to quickly understand the code that uses this pattern. In addition, to deepen the understanding of Visitor Pattern, I will also describe **how the Visitor Pattern was born.**


> Most design patterns are simple and easy to understand, and they make code more readable and easier to maintain. 
> 
> But the visitor pattern is not. **It's hard to understand, hard to implement,** and it makes code less readable and less maintainable. **This is because the Visitor Pattern was born from the defect,** and it emerged to compensate for the shortcomings of Single Dispatch languages.
{: .prompt-tip }

**Through this blog, you will better understand:** [why are design principles more important than design patterns?](/posts/Design-Principles/). If you don't understand the design principles, you're likely to use the Visitor Pattern in a wrong way.

> In real-world development, **do not use the Visitor Pattern unless you have strong reasons to do so.**
>
> A lot of developers apply Visitor Pattern just to show off. This doesn't do any good and only makes the code quality worse.
{: .prompt-warning }

---

<center><font size='5'> Contents </font></center>

---

<!-- TOC -->
  * [What is the Visitor Pattern?](#what-is-the-visitor-pattern)
    * [Key Components](#key-components)
  * [Why Do We Need the Visitor Pattern?](#why-do-we-need-the-visitor-pattern)
  * [How the Visitor Pattern was Born: to Compensate for a Defect](#how-the-visitor-pattern-was-born-to-compensate-for-a-defect)
    * [Implement Pseudo-Dynamic Overloading via `this` Pointer](#implement-pseudo-dynamic-overloading-via-this-pointer)
    * [Business Decoupling Using the Abstract Interface `Visitor`](#business-decoupling-using-the-abstract-interface-visitor)
  * [The Visitor Pattern Violates Most Design Principles, Acting like an Anti-pattern](#the-visitor-pattern-violates-most-design-principles-acting-like-an-anti-pattern)
<!-- TOC -->

---

## What is the Visitor Pattern?

> Visitor Pattern: 
> 
> Allows for one or more **operation to be applied to a set of objects at runtime**, decoupling the operations from the object structure.

The **Visitor Pattern** is a behavioral design pattern that separates algorithms from the objects on which they operate. (This is similar to the Strategy Pattern, but more complex.) In this pattern, you create a visitor object that "visits" other objects in a class hierarchy. Each object in the hierarchy has an `accept()` method, which takes a visitor as an argument. The visitor then applies an operation to the object based on its type.

### Key Components

1. **Visitor Interface**: Defines operations for each type of element in the object structure.
2. **Concrete Visitor**: Implements the operations defined in the visitor interface.
3. **Element Interface**: Defines an `accept()` method that takes a visitor object.
4. **Concrete Elements**: Classes in the object structure that implement the `accept()` method and allow the visitor to perform operations.

## Why Do We Need the Visitor Pattern?

This is because: **`overloading` cannot be dynamically bound in single dispatch languages**. 

As mentioned above, Visitor Pattern **operates on objects based on their type.** This seems easy as we can easily implement it based on `overloading`. 

---

Suppose there is a scenario: we need to calculate the shape area based on different types of shapes. We can do this by `overloading`:

```java
abstract class Shape {
    // ...
}

class Circle extends Shape {
    public double radius;

    public Circle(double radius) {
        this.radius = radius;
    }
}

class Rectangle extends Shape {
    public double width, height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
}

class Calculator {
    // overloading
    public void calculateArea(Circle circle) {
        System.out.println("Circle Area: " + Math.PI * circle.radius * circle.radius);
    }

    // overloading
    public void calculateArea(Rectangle rectangle) {
        System.out.println("Rectangle Area: " + rectangle.width * rectangle.height);
    }
}

public class Main {
    public static void main(String[] args) {
        Shape circle = new Circle(5);
        Shape rectangle = new Rectangle(4, 6);

        Calculator calculator = new Calculator();
        calculator.calculateArea(circle);
        calculator.calculateArea(rectangle);
    }
}
```

As shown in the code above, we just need to overload the method `calculateArea`. This way `calculateArea` can perform different operations based on the different types of input parameters. **But if this could really be done, then we wouldn't need the Visitor Pattern.**

If you are familiar enough with Java, you'll realise that the code above won't compile successfully, and **lines 40 and 41 will report errors.** This is because **`overloading` cannot be dynamically bound in Java, which is the single dispatch language**. (In the double dispatch language, the above code will compile successfully.)

> The Visitor Pattern was created to compensate for this defect: single dispatch languages don't support dynamic overloading.
{: .prompt-tip }

> - **What is `Dispatch`?**
>   - In OOP, we can understand `dispatch` as **message passing at runtime**, also known as **method invocation at runtime.**
>   - In OOP, we can make invocations of methods **at runtime (dynamic)** in two ways: **overloading** and **overriding**. Both are manifestations of **polymorphism** in OOP.
> 
> <br>
>
> - **What is Single Dispatch?**
>   - **Single Dispatch: Only support one type of dynamic method invocation (overriding).**
>   - In single dispatch languages, such as Java, Python, or C++, method invocation is based only on the **runtime type of the object receiving the call (the receiver)**.
>   - Most of the current mainstream languages are single dispatch languages.
> - **What is Double Dispatch?**
>   - **Double Dispatch: Support two types of dynamic method invocation (overriding and overloading).**
>   - In double dispatch languages, such as Clojure or Julia, method invocation is based both on the **runtime types of the receiver and the parameters.**
>   - Double dispatch languages don’t need Visitor Pattern because they support dynamic overloading.
{: .prompt-info }
 
## How the Visitor Pattern was Born: to Compensate for a Defect

As mentioned above, the Visitor Pattern is used to solve the problem that overloading cannot be bound dynamically. But how?

### Implement Pseudo-Dynamic Overloading via `this` Pointer

> **The core idea of Visitor Pattern is to implement pseudo-dynamic overloading via `this` pointer.**
{: .prompt-tip }

As shown below, we can add an abstract method `accept()` in the parent class `Shape` that receives `Calculator`. Then we implement this method in each of the subclasses and pass the subclass's `this` pointer to the `calculateArea` method in `Calculator`. This is a smart implementation of pseudo-dynamic overloading, **which is key to understanding the Visitor Pattern**.

```java
abstract class Shape {
    // Other codes remain unchanged
   
    public abstract void accept(Calculator calculator);
}

class Circle extends Shape {
    // Other codes remain unchanged

    @Override
    public void accept(Calculator calculator) {
        calculator.calculateArea(this);
    }
}

class Rectangle extends Shape {
    // Other codes remain unchanged

    @Override
    public void accept(Calculator calculator) {
        calculator.calculateArea(this);
    }
}

// The code of Calculator remains unchanged

public class Main {
    public static void main(String[] args) {
        Shape circle = new Circle(5);
        Shape rectangle = new Rectangle(4, 6);

        Calculator calculator = new Calculator();
        circle.accept(calculator);
        rectangle.accept(calculator);
    }
}
```

### Business Decoupling Using the Abstract Interface `Visitor`

The above code solves the problem that overloading cannot be bound dynamically, but the code is not extensible. For example, if we need to add a new feature: print shape type, we have to add `accept()` methods in both parent and child classes: 

```java 
abstract class Shape {
    // Other codes remain unchanged

    public abstract void accept(Calculator calculator);
    public abstract void accept(Printer printer);
}

class Circle extends Shape {
    // Other codes remain unchanged

    @Override
    public void accept(Calculator calculator) {
        calculator.calculateArea(this);
    }

    @Override
    public void accept(Printer printer) {
        printer.printType(this);
    }
}

class Rectangle extends Shape {
    // Other codes remain unchanged

    @Override
    public void accept(Calculator calculator) {
        calculator.calculateArea(this);
    }

    @Override
    public void accept(Printer printer) {
        printer.printType(this);
    }
}

// The code of Calculator remains unchanged

class Printer {
    // overloading
    public void printType(Circle circle) {
        System.out.println("This is Circle");
    }

    // overloading
    public void printType(Rectangle rectangle) {
        System.out.println("This is Rectangle");
    }
}
```

**This violates the OCP, and this can lead to classes frequently needing to be modified and constantly getting bigger.**

How can we solve this problem? **We can abstract a `Visitor` interface and make the `accept()` depend on the abstraction.** This allows `Shape` and its subclasses to be **decoupled** from the operation business, and no longer need to follow the changes in the operation business. 

```java 
// Visitor interface
interface Visitor {
    void visit(Circle circle);
    void visit(Rectangle rectangle);
}

// Concrete Visitor
class AreaCalculator implements Visitor {
    @Override
    public void visit(Circle circle) {
        System.out.println("Circle Area: " + Math.PI * circle.radius * circle.radius);
    }

    @Override
    public void visit(Rectangle rectangle) {
        System.out.println("Rectangle Area: " + rectangle.width * rectangle.height);
    }
}

class TypePrinter implements Visitor {
    @Override
    public void visit(Circle circle) {
        System.out.println("This is Circle");
    }

    @Override
    public void visit(Rectangle rectangle) {
        System.out.println("This is Rectangle");
    }
}

// Element interface
abstract class Shape {
    public abstract void accept(Visitor visitor);
}

// Concrete Elements
class Circle extends Shape {
    public double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}

class Rectangle extends Shape {
    public double width, height;

    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}

// Main class
public class Main {
    public static void main(String[] args) {
        Shape circle = new Circle(5);
        Shape rectangle = new Rectangle(4, 6);

        Visitor areaVisitor = new AreaCalculator();
        circle.accept(areaVisitor);
        rectangle.accept(areaVisitor);

        TypePrinter typePrinter  = new TypePrinter();
        circle.accept(typePrinter);
        rectangle.accept(typePrinter);
    }
}
```

## The Visitor Pattern Violates Most Design Principles, Acting like an Anti-pattern

**Because the Visitor pattern was created to compensate for a defect, it has many drawbacks and violates many design principles:**

- **Extra Complexity**
  - The Visitor Pattern introduces extra complexity, particularly in large or deeply nested object hierarchies. This makes the code difficult to understand.
- **Tight Coupling Between Visitor and Object Structure**
  - Visitors need to know about the concrete types in the object hierarchy to implement the correct operations. This makes the system less flexible and harder to extend, especially when the object structure changes.
- **Violation of the Law of Demeter (LoD).**
  - When using the Visitor Pattern, the `accept()` method of an object passes the entire object to the visitor, effectively allowing the visitor to operate on its internal data. This breaks the Law of Demeter, as external objects (visitors) now need to know the internal structure of the class to operate on it. If some attributes of the visited object are increased/decreased, all visitors may need to make changes as well.
- **Violation of the Open/Closed Principle (OCP)**
  - When you add a new class to the object hierarchy (e.g., a `Triangle` class), you must modify the existing visitor interface and all of its concrete visitor implementations to account for the new class.
- **Violation of the Single Responsibility Principle (SRP)**
  - The visitor class is responsible for handling multiple types of objects. A visitor can become a dumping ground for many operations, leading to classes with too many responsibilities.
- **Violation of the Dependency Inversion Principle (DIP)**
  - In the Visitor pattern, the Visitor must provide a specific `visit()` method for each concrete element class, which means that the Visitor depends on these concrete classes. This leads to all Visitors having to be modified no matter if an element class is added or removed.
- **Violation of the Interface Segregation Principle (ISP)**
  - The Visitor interface needs to provide `visit()` methods for all element classes, which could potentially lead to some concrete Visitor class being forced to rely on methods it doesn't need.

> In practice, we don't need to strictly adhere to all design principles, but Visitor Pattern conflicts with most of them. This results in the Visitor Pattern being very much like an anti-pattern.
{: .prompt-tip }


---

**Reference:**

- Wang, Zheng (2019) _The Beauty of Design Patterns_. Geek Time. 
- https://refactoring.guru/design-patterns/visitor







