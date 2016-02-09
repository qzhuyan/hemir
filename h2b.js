//hemnet to bocker
// option: --url='balalbalba
var casper = require('casper').create();
var url = casper.cli.get('url');
casper.log('url is ' + url,'debug');
delimiter='||';
casper.start(url,function() {
    var bidding = this.exists('div[class="property__flags clear-children"]');
    if (bidding) {
	bidding = this.getElementAttribute('div[class="property__flags clear-children"] div a', 'href');
    }
	
    var broker = this.getElementAttribute('a[class="button right"]','href');
    this.echo( bidding + delimiter + url+ delimiter+ broker);
});

casper.run();


