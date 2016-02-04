var casper = require('casper').create();
casper.start('http://hemnet.se', function()
	     {
		 casper.viewport(1500, 1080);
		 this.echo("in 1st step");
		 this.mouseEvent('click', 'a[class="dropdowns-action"]');
		 this.capture('1nd.png',{top:0, left:0, width:800, height:1024})
		 this.fill('form[action="/sok/create"]',
			   {'search\[region_id\]': '17744'},
			   false);
		 this.mouseEvent('click', 'button[name="commit"]');
	     });


casper.then(function() {
    this.echo("in 2nd step");
    this.echo(this.getTitle());
    this.capture('2nd.png',{top:0, left:0, width:800, height:1024})
});

	     
casper.run();
