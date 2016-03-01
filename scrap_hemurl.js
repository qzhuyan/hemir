//hemnet to bocker
// option: --hems='url1 url2 url3'
var fs = require('fs');

var casper = require('casper').create(
    { stepTimeout: 10000,
      waitTimeout: 10000,
      pageSettings: { webSecurityEnabled: false },
      onStepTimeout: function(self,m){
      	  console.log('timeout: step' + m);
      }
    });


casper.userAgent('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36');

var urls = casper.cli.get('hems').split(' ');


function imgurl2local(url) {
    return url.substr(url.lastIndexOf('/') + 1);
}

casper.echo('urls are ' + urls);

function save_imgs(dir) {
    casper.echo('save imgs...')
    var srcList = [];
    srcList = casper.evaluate(function(){
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
    	casper.download(imgurl, dir + '/' + shorturl);
    };
    casper.then(function() {save_html(dir)})
}

function save_html(dir) {
    casper.echo('save html...')
    var html = casper.getPageContent();
    var f = fs.open(dir + '/index.html', 'w');
    f.write(html);
    f.close();
    var broker = casper.getElementAttribute('a[class="button right"]','href');
    if (broker && ! (broker.indexOf(".erikolsson.se") >= 0)) {
	casper.echo("broker url is " + broker);
	casper.then(function() {scrap_hem_page(broker)})
    }
}


function scrap_hem_page(url) {
    casper.echo('scrap url:'+url);
    casper.thenOpen(url, function() {
	casper.echo('scraped url:'+url);
	casper.then( function() {
	    casper.then(function() { save_imgs(url)});
	});
    });
}

casper.start()
    .then(function () {
	urls.forEach(scrap_hem_page);
    });

casper.run();


