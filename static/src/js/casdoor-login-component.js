const {useState} = owl.hooks;
const {xml} = owl.tags;
import SDK from './casdoor-js-sdk.js'

class DferpCasdoorSiteAuth extends Component {
    setup() {
        this.state = useState({value: 1});
        this.sdkConfig = {
            serverUrl: "https://door.casbin.com",
            clientId: "014ae4bd048734ca2dea",
            appName: "app-casnode",
            organizationName: "casbin",
            redirectPath: "/callback",
            signinPath: "/api/signin",
        }
        this.sdk = new SDK(this.sdkConfig);
    }

    signin() {
        this.sdk
            .popupSignin("https://door.casbin.com", "/api/signin")
            .then((account) => {
            });
    }
}

DferpCasdoorSiteAuth.template = 'df_erp_casdoor_site_auth.DferpCasdoorSiteAuth';