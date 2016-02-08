//hemnet to bocker
// option: --url='balalbalba
var casper = require('casper').create();
var url = casper.cli.get('url');
casper.log('url is ' + url,'debug');
delimiter='||';
casper.start(url,function() {
    var isbidding = this.exists('div[class="ribbon right ongoing-bidding"]');
    var broker = this.getElementAttribute('a[class="button right"]','href');
    this.echo( isbidding + delimiter + broker);
});

casper.run();


