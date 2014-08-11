var test = JSON.parse(json_str);


/* FUNCTION FOR SENDING COMMANDS TO SERVER */
/* Resets Command object if succesful */

function sendCommand(cmd, game_name, simple){
    $.ajax('/submit', 
        {data: JSON.stringify({commands: cmd,
                game: game_name}), 
        type:'POST', 
        dataType:'json', 
        contentType: 'application/json',
        success: function(data){
            //$('#splendid').html("<pre>" + data['summary'] + "</pre>");
            console.log(data)
            if (data['error_code']) {alert(data['value']);}
            else {
                Command.reset();
                if (!simple) update_board(data); //update_board(data);
                else splendid.append('<pre>' + data['summary'] + '</pre>');
            }        
        }
    })
}


/* PARSING FUNCTIONS FOR CREATING BOARD */
function parse_gems(Gems, key, template){
    // For each gem in Gems object, add list element with gem count
    // append to ul in template
    $.each(Gems, function(ii, val){
        if (ii == 'B') var cls = 'BB';
        else var cls = ii;
        var gem_el = template.find('.p-' + key);
        var li = $("<li></li>");
        var quant = $("<span></span>");
        li.addClass('gem-' + cls);
        quant.addClass('vertical-center').html(val);
        li.append(quant);
        gem_el.append(li);
    });
}

function gen_player_card(player, landcard, target, is_current){
    if (is_current) target.attr('id', 'myturn');
    target.find('.p-points').html('points: ' + player['points']);
    target.find('.p-name').html(player['name']);
    parse_gems(player['gems'], 'wallet', target);
    parse_gems(player['land_bonus'], 'land_bonus', target);
    var cardlist = target.find('.lands');
    gen_land_cards(player['lands'], landcard, cardlist, 'land-', true);
}

function parse_land(Land, card, id_pre, showcost){
    // For Land object 
    if(typeof(showcost)==='undefined') showcost = true;
    // Add content
    if (showcost) parse_gems(Land['cost'], 'gems', card);
    card.find('.c-id').html(Land['id']);
    card.find('.c-pv').html(Land['pv']);
    card.find('.c-type').html(Land['type']);
    // Add ID and Class attributes
    card.attr('id', id_pre + Land['id']);
    if (Land['type'] == 'B') var type = 'BB';
    else var type = Land['type'];
    card.addClass('type-' + type + " " + "tier-" + Land['tier'])
    //console.log(id_pre + Land['type'])
}

function gen_land_cards(Lands, template, target, id_pre, showcost){
    // Lands: array of land objects
    // template: html template to copy
    // target: element to copy filled out template in to
    var newcard;
    for (var ii=0; ii < Lands.length; ii++){
        newcard = template.clone();
        parse_land(Lands[ii], newcard, id_pre, showcost);
        target.append(newcard);
    }
}

/* MAIN FUNCTION FOR UPDATING BOARD*/
//data = JSON.parse(json_str);
splendid = $('#splendid');
playersDiv = splendid.find('#player-wrapper');
boardDiv = splendid.find('#board-wrapper');
bankDiv = splendid.find('#bank-wrapper');
var glob;

function update_board(data){
    playersDiv.empty();
    boardDiv.empty();
    bankDiv.empty();
    glob = data;
    $.get('/_/template.html', function(template){
        template = $(template)
        var landtemp = template.closest('.c-land');

        // Generate each player
        for (pname in data['players']){
            var player = data['players'][pname];
            var playercard = template.closest('.player').clone();
            var is_current = player.name == data['crnt_player'];
            gen_player_card(player, landtemp, playercard, is_current);

            playersDiv.append(playercard);
        }

        // Generate Bank
        var bank = template.closest('#bank-gems');
        parse_gems(data['bank'], 'bank', bank);
        bankDiv.append(bank);
        
        
        // Generate Board
        var board = template.closest('#board')
        for (var ii=0; ii < data['decks'].length; ii++){
            deck = data['decks'][ii];
            var deck_out = board.find('#tier-' + deck['tier'])
            gen_land_cards(deck['table'], landtemp, deck_out, 'land-');
        }
        noble_out = board.find('.nobles');
        gen_land_cards(data['nobles'], landtemp, noble_out, 'noble-');
        boardDiv.append(board)


        
        
    });
}

/* FOR UI CLICK TO COMMANDS */
Command = {
    gems: {},
    ttlgems: 0,
    reset: function(){
        this.ttlgems = 0;
        var gemtypes = 'rgbBWA';
        for (var ii=0; ii < gemtypes.length; ii++) this.gems[gemtypes[ii]] = 0;
        this.landCard = "";
        this.gemSource = "";
    },
    options: function(){
        var todo = {};
        todo['buy'] = (this.landCard != "") & (this.gemSource == 'wallet');
        todo['reserve'] = this.landCard != "" & this.ttlgems == 0;
        todo['draw'] = this.landCard == "" & this.ttlgems > 1;
        return todo
    },
    addGem: function(gem, source){
        if (!this.gemSource | source != this.gemSource) {
            var prev_landcard = this.landCard;
            this.reset();
            this.landCard = prev_landcard;
            this.gemSource = source;
            this.addGem(gem, source);
            return
        }
        this.gems[gem] += 1;
        this.ttlgems +=1;
    },
    addLand: function(landCard){
        if (this.landCard == landCard) this.landCard = "";
        else this.landCard = landCard;
    },
    genCommand: function(cmd){
        cmd = String(cmd).toLowerCase();
        var gem_str = "";
        for (k in this.gems) gem_str += Array(this.gems[k] + 1).join(k);
        if (!this.landCard) return cmd + " " + gem_str;
        else                return cmd + " " + this.landCard + " " + gem_str;
    },
    updateOptions: function(){
        div = $('#game-header');
        var moves = div.find('[id^="do"]');
        var options = this.options()
        
        for (var ii=0; ii < moves.length; ii++){
            var el = $(moves[ii]);
            var move = String(el.attr('id')).replace('do-',"");
            glob = el;
            if (options[move]){
                el.addClass('available');
            }
            else el.removeClass('available');
        }
    },
    updateSelected: function(){
        var div = $('#move-selected');
        div.find('.p-selected').html("");
        var crnt_gems = {};
        for (k in this.gems){
            if (this.gems[k] > 0) crnt_gems[k] = this.gems[k];
        }
        div.find('#gem-source span').html(this.gemSource);
        
        parse_gems(crnt_gems, 'selected', div);
        
        $('.selected').removeClass('selected');
        $('#land-'+this.landCard).addClass('selected');
    }
}
