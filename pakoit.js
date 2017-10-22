var fs = require('fs');
var pako = require('pako');
var path = require('path');
const PATH = path.join('outcome', 'temppostdata.js')
const OUTPATH = path.join('outcome', 'postdata.js')
const PAKORAW = path.join('outcome', 'pako_rawpostdata.js')
var file = fs.readFile(PATH, 'utf-8', (err, data) => {
    if (err) throw (err);
    cdata = data.split(";");
    //console.log(cdata[0]);
    var jsondata = JSON.parse(cdata[0]);
    var pakodata = pako.deflate(jsondata['post']['content']);
    jsondata['post']['content'] = pakodata;
    var outpakodata = JSON.stringify(jsondata) + ';'
    fs.writeFile(PAKORAW, outpakodata, { flag: 'a+' });
    fs.readFile(PAKORAW, 'utf-8', (err, data) => {
        var outarray = [];
        var cdata = data.split(";")
        cdata.pop(0);
        for (var i = 0; i < cdata.length; i++) {
            var jsondata = JSON.parse(cdata[i]);
            var pakodata = pako.deflate(jsondata['post']['content']); //{ to: 'string' }
            jsondata['post']['content'] = pakodata
            var outdata = JSON.stringify(jsondata)
            outarray.push(outdata);
            var outdata = " var post = function() {\
                var data = " + outarray + ";return data\
                } ";
            fs.writeFile(OUTPATH, outdata);
        }
    });
    console.log('pako finish');
});