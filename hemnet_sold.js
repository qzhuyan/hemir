url="http://www.hemnet.se/salda/bostader?location_ids%5B%5D=18028&region_id=17744";

var casper = require('casper').create(
    { pageSettings: { webSecurityEnabled: false ,
		      loadImages: false,
		      loadPlugins: false
		    }} );
soldlink='';
casper.options.onResourceRequested = function(casper, requestData, request)
{
    if (!/.*hemnet.*/.test(requestData.url))
    {
	request.abort();
    }
}

var links = [];

function capture_to(file) {
    casper.capture(file,{
        top: 100,
        left: 100,
        width: 1024,
        height: 1024
    });
}


function getLinks() {
    var links = document.querySelectorAll('.item-link-container');
    return Array.prototype.map.call(links, function(e) {
	var v = e.getAttribute('href');
	return v;
    });
}

function getsold() {
    return document.querySelector('.active').childNodes[1].getAttribute('href');

};

var follow_next_button = function() {
    links = links.concat(this.evaluate(getLinks));
    if (this.exists('a[class="next_page button button--primary"]'))
    {
	this.thenClick('a[class="next_page button button--primary"]',
		       function() { this.then(follow_next_button);});
    } else {
	this.log("follow button finished!",'debug');
    }
};

casper.start('http://www.hemnet.se/salda/bostader?location_ids%5B%5D=18028', follow_next_button);
// casper.start('http://hemnet.se', function() {
//     casper.viewport(1500, 1080);

//     this.mouseEvent('click', 'a[class="dropdowns-action"]');

//     this.fillXPath('form[action="/bostader"]', {
// 	//'//select[@id="search_region_id"]': '17744', //stockholm
// 	'//input[@id="search_municipality_ids_18028"]': true //solna
//     },false);

//     this.mouseEvent('click', 'button[class="button button--primary js-submit-button right"]');
// });

// casper.then(function() {
//     soldlink = 'http://www.hemnet.se/salda/'+this.evaluate(getsold);
//     this.echo(soldlink);
//     //thenOpen(soldlink,follow_next_button);
// });
//casper.Open('',follow_next_button);
casper.run(function() {
    this.log(links.length + ' links found:','info');

    links = links.map(function(link) {
	return link;
    });

    this.echo(links.join('\n'));
    
    this.exit();

});
