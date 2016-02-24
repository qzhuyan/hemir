//hemnet to bocker
// option: --url='balalbalba
var fs = require('fs');

var casper = require('casper').create(
    { pageSettings: { webSecurityEnabled: false }} );

var url = casper.cli.get('url');

var dir = url;

casper.log('url is ' + url,'debug');
delimiter='|';

casper.userAgent('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36');
casper.start(url,function() {
    var bidding = this.exists('div[class="property__flags clear-children"]');
    if (bidding) {
	bidding = this.getElementAttribute('div[class="property__flags clear-children"] div a', 'href');
    }
	
    var broker = this.getElementAttribute('a[class="button right"]','href');
    this.echo( bidding + delimiter + url+ delimiter+ broker);
});


function imgurl2local(url) {
    return url.substr(url.lastIndexOf('/') + 1);
}


casper.then(function(){
    var srcList = [];
    srcList = this.evaluate(function(){
	var images = document.getElementsByTagName('img');
	var res = [];
	for(var i = 0; i < images.length; i++) {
	    var raw = images[i].src;
	    res.push(raw);
	    //images[i].src = imgurl2local(raw);
	}
	return res;
    });
    for(var i=0 ; i<srcList.length; i++) {
    	var imgurl = srcList[i];
    	var shorturl = imgurl2local(imgurl);
    	casper.log("downloading\n" + imgurl,'debug');
    	this.download(imgurl, dir + '/' + shorturl);
    };
});


casper.then(function() {
    var html = this.getPageContent();
    var f = fs.open(dir + '/index.html', 'w');
    f.write(html);
    f.close();
});

casper.run();


