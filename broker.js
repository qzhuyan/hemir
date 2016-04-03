// scrape page from broker's website
// option: --url='balalbalba
var fs = require('fs');

var casper = require('casper').create(
    { pageSettings: { webSecurityEnabled: false ,
		      loadImages: false,
		      loadPlugins: false
		    }} );

casper.options.waitTimeout = 10000;

var url = casper.cli.get('url');

var dir = "broker/"+url;

casper.log('url is ' + url,'debug');

casper.userAgent('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36');

casper.start(url, function afterStart() {
    // casper.log("start loading "+url, 'debug');
    // this.capture('foo', undefined, {
    //     format: 'jpg',
    //     quality: 75});
});

function imgurl2local(url) {
    return url.substr(url.lastIndexOf('/') + 1);
}

casper.then(function(){
    casper.log("start find images ", 'debug');
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
	var filePath = dir + '/' +shorturl;
	casper.log("working on: "+ filePath, 'debug');	
	if (!fs.exists(filePath))
	{
	    casper.log("downloading\n" + imgurl,'debug');
    	    this.download(imgurl, filePath);
	} else {
	    casper.log("skip downloading"+filePath,'debug');
	}
	
    };
});


casper.then(function() {
    var html = this.getPageContent();
    var f = fs.open(dir + '/index.html', 'w');
    f.write(html);
    f.close();
});

casper.run();

