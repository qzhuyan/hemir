var casper = require('casper').create();
var links = [];
var fs = require('fs');
function getLinks() {
    var links = document.querySelectorAll('.item-link-container');
    return Array.prototype.map.call(links, function(e) {
	var v = e.getAttribute('href');
	return v;
    });
}

var follow_next_button = function() {
    links = links.concat(this.evaluate(getLinks));
    if (this.exists('a[class="next_page button button--primary"]'))
    {
	this.thenClick('a[class="next_page button button--primary"]',
		       function() {this.then(follow_next_button);});
    } else {
	this.log("follow button finished!",'debug');
    }
};

casper.start('http://hemnet.se', function() {
    casper.viewport(1500, 1080);
    this.mouseEvent('click', 'a[class="dropdowns-action"]');
    this.fillXPath('form[action="/sok/create"]', {
	'//select[@id="search_region_id"]': '17744', //stockholm
	//'//input[@id="search_municipality_ids_18028"]': true //solna
    },false);

    this.mouseEvent('click', 'button[name="commit"]');
});

casper.then(follow_next_button);

casper.run(function() {
    this.log(links.length + ' links found:','info');
    links = links.map(function(link) {
	return 'http://www.hemnet.se' + link
    });
    this.echo(links.join('\n'));

    var len = links.length;
    
    var data1 = links.slice(0,len/2).join('\n');
    this.echo("\n==================\n");
    this.echo(data1);
    var f = fs.open('./1.data','w');
    f.write(data1);
    f.close();
    
    this.echo("\nxxxxxxxxxxxxxxxxxxxx\n");
    var data2 = links.slice(len/2+1,len).join('\n');
    this.echo(data2);
    var f = fs.open('./2.data','w');
    f.write(data2);
    f.close();
    this.exit();

});
