/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');
 const DetailKeys = [
    "id",
    "city",
    "state",
    "st",
    "address",
    "zip",
    "lat",
    "long"
    ];


 async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
    });
 
 
    try {
        let dbList = await cloudant.db.use("dealerships").list({include_docs:true});
        dbList = dbList["rows"];
        let dbDealers = [];
        let details = {};
        let keys;
        for (var i = 0; i < dbList.length; i++) {
            keys = Object.keys(dbList[i]["doc"]);
            for (var y = 0; y < keys.length; y++) { 
                if (DetailKeys.includes(keys[y])) {
                    details[keys[y]] = dbList[i]["doc"][keys[y]]
                };
            };
            dbDealers.push(details);
            details = {};                
        };
        return { dbDealers } ;
    } catch (error) {
        return { error: error.description };
    }
 
 }