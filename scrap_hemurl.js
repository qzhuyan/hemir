//hemnet to bocker
// option: --hems='url1 url2 url3'
var fs = require('fs');

var casper = require('casper').create(
    { stepTimeout: 20000,
      waitTimeout: 20000,
      pageSettings: {
	  loadImages:  false,        // do not load images
          loadPlugins: false,         // do not load NPAPI plugins (Flash, Silverlight, ...)
	  webSecurityEnabled: false },

      onStepTimeout: function(self,m){
      	  console.log('timeout: step' + m);
      }
    });


casper.userAgent('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36');

//var urls = casper.cli.get('hems').split(' ');

var datafile = casper.cli.get('data')
var urls  = fs.read(datafile).split('\n')

function imgurl2local(url) {
    if (url.slice(-1) == '/') {
	url = url.slice(0,-1)
	return url.substr(url.lastIndexOf('/') + 1);
    } else {
	return url.substr(url.lastIndexOf('/') + 1);
    }
}

function save_imgs(dir) {
    var srcList = [];
    srcList = casper.evaluate(function(){
	var images = document.getElementsByTagName('img');
	var res = [];
	for(var i = 0; i < images.length; i++) {
	    var raw = images[i].src 
	    if (raw != '') {
		res.push(raw);
	    } else {
		casper.echo("!!!!!! cannot find src for image !!!")
	    }
	}
	return res;
    });
    for(var i=0 ; i<srcList.length; i++) {
    	var imgurl = srcList[i];
    	var shorturl = imgurl2local(imgurl);
    	casper.log("downloading\n" + imgurl ,'debug');
    	casper.download(imgurl, dir + '/' + shorturl);
    };
    casper.then(function() {save_html(dir)})
}

function save_html(dir) {
    var html = casper.getPageContent();
    var f = fs.open(dir + '/index.html', 'w');
    f.write(html);
    f.close();
    var broker = casper.getElementAttribute('a[class="button right"]','href');
    if (broker && ! (broker.indexOf(".erikolsson.se") >= 0)) {
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


