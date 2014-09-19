View selector widget: custom faceted navigation widget
======================================================

This widget provides a widget that allows the user to chose how he wants to
view the results: as a list or as squares.

For it to work, each result item should be wrapped like this:
    
    <div class="span12 view1 item_wrapper">

        ...

    </div>

So when user clicks on the widget link to change the view, we replace with
jquery the classes "span12 view1" with "span4 view2".
