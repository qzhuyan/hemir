var casper = require('casper').create(
    { pageSettings: { webSecurityEnabled: false ,
		      loadImages: false,
		      loadPlugins: false
		    }} );
var links = [];

function getLinks() {
    var links = document.querySelectorAll('.item-link-container');
    return Array.prototype.map.call(links, function(e) {
	var v = e.getAttribute('href');
	return v;
    });
}

var follow_next_button = function() {
    casper.capture('hemnet2.jpg',{
        top: 100,
        left: 100,
        width: 1024,
        height: 1024
    });

    links = links.concat(this.evaluate(getLinks));
    if (this.exists('a[class="next_page button button--primary"]'))
    {
	this.thenClick('a[class="next_page button button--primary"]',
		       function() { this.then(follow_next_button);});
    } else {
	this.log("follow button finished!",'debug');
    }
};


// casper.options.onResourceRequested = function(casper, requestData, request)
// {
//     request.abort();
// }

casper.start('http://hemnet.se', function() {
    casper.viewport(1500, 1080);

    this.mouseEvent('click', 'a[class="dropdowns-action"]');
            casper.capture('hemnet.jpg',{
        top: 100,
        left: 100,
        width: 1024,
        height: 1024
    });

    this.fillXPath('form[action="/bostader"]', {
	//'//select[@id="search_region_id"]': '17744', //stockholm
	'//input[@id="search_municipality_ids_18028"]': true //solna
    },false);
    casper.capture('hemnet2.jpg',{
        top: 100,
        left: 100,
        width: 1024,
        height: 1024
    });

    this.mouseEvent('click', 'button[class="button button--primary js-submit-button right"]');
});

casper.then(follow_next_button);

casper.run(function() {
    this.log(links.length + ' links found:','info');

    links = links.map(function(link) {
	return 'http://www.hemnet.se' + link
    });

    this.echo(links.join('\n'));
    
    this.exit();

});
