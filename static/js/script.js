$(document).ready(function() {
    var ingredients = [];
    var colors = ['', 'blue', 'pink', 'orange'];

    // Add ingredient when the "Add Ingredient" button is clicked
    $('#add-ingredient').on('click', function() {
        addIngredient($('#ingredient-input').val());
    });

    // Add ingredient when Enter key is pressed in the input field
    $('#ingredient-input').on('keypress', function(e) {
        if (e.which == 13) {
            e.preventDefault();
            addIngredient($(this).val());
        }
    });
    
    // Function to add ingredients in different colors
    function addIngredient(ingredient) {
        ingredient = ingredient.trim();
        if (ingredient && !ingredients.includes(ingredient)) {
            ingredients.push(ingredient);
            var colorClass = colors[Math.floor(Math.random() * colors.length)];
            $('#ingredients-list').append(
                `<div class="ingredient-item ${colorClass}">
                    ${ingredient}
                    <span class="remove-ingredient">&times;</span>
                </div>`
            );
            $('#ingredient-input').val('');
            console.log("Added ingredient:", ingredient);
            console.log("Current ingredients:", ingredients);
        }
    }

    $(document).on('click', '.remove-ingredient', function() {
        var ingredient = $(this).parent().text().slice(0, -1).trim();
        ingredients = ingredients.filter(item => item !== ingredient);
        $(this).parent().remove();
        console.log("Removed ingredient:", ingredient);
        console.log("Current ingredients:", ingredients);
    });

    // Add click event for the "Search for Recipe" button
    $('#search-recipe').on('click', function() {
        console.log("Search clicked. Ingredients:", ingredients);
        // Create a form and submit it if there are ingredients
        if (ingredients.length > 0) {
            var form = $('<form action="/recipes" method="post"></form>');
            form.append($('<input type="hidden" name="ingredients">').val(ingredients.join(',')));
            $('body').append(form);
            form.submit();
        }
        // No alert or error message is shown if no ingredients are present
    });
    // Autocomplete functionality
    $("#ingredient-input").autocomplete({
        source: function(request, response) {
            $.getJSON("/get_ingredients", {
                query: request.term
            }, function(data) {
                response(data);
            });
        },
        minLength: 2,
        select: function(event, ui) {
            event.preventDefault();
            addIngredient(ui.item.value);
        }
    });
});
