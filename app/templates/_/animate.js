$(document).ready(function(){
	
	$(document).on('click', '.lands-container', function(){
		var pLands = $(this).find('.p-lands')
		pLands.toggle();
		pLands.draggable();
		pLands.prepend('<button id=button>X</button>');
		
	});
		
	$(document).on('click', "#button", function(){
		var pLands = $(this).find('.p-lands')
		pLands.toggle();
	});

    $(document).on('click', '[class^="gem-"]', function(){
        console.log('CLICKITY CLACK');
        el = this;
        // check if str wallet is in classname
        if (el.parentElement.className.indexOf('wallet') != -1){
            var gemSource = 'wallet';
        }
        else gemSource = 'bank';
        // get gem type
        indx = el.className.length - 1
        var gem = el.className[indx]; // this seems fragile

        console.log('gem clicked');
        Command.addGem(gem, gemSource);
        Command.updateOptions();
        Command.updateSelected();
    });

    $(document).on('click', '.b-lands .c-land', function(){
        id = String(this.id).replace('land-', "");
        console.log('land clicked');
        console.log('previous id: ' + Command.landCard);
        console.log('new id: ' + id);
        // update Command object
        Command.addLand(id);
        Command.updateOptions();
        Command.updateSelected();
    });




	// $('.lands-container').on('click', function(){
	// 	var pLands = $(this).find('.p-lands')
	// 	pLands.toggle();
	// 	pLands.draggable();
	// 	pLands.prepend('<button id=button>X</button>');
		
	// });
		
	// $('#button').on('click', function(){
	// 	var pLands = $(this).find('.p-lands')
	// 	pLands.toggle();
		
		
		
	// });
	
	//move h3 nobles text into DIV
	
	var noblesTitle = $('#board').last('h3').text();
	$('#board').find('h3').last().remove();
		
	//move nobles div out of board div (needs persistant visible)
	//find div and copy
	
	var noblesDiv = $('#board').find('div.nobles').clone();
	$('#board').find('div.nobles').detach();
	
	//put noblesDiv at end of boardwrapper
	
	$('#board-wrapper').append(noblesDiv);
	
	
	
	
});
