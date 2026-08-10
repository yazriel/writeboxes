let a = !1;
async function p() {
    const o = Date.now();
    return new Promise((r, i) => {
        const c = () => {
            if (typeof gapi < "u" && typeof gapi.load == "function") {
                r();
                return
            }
            if (Date.now() - o > 15e3) {
                i(new Error("Timeout waiting for gapi to load"));
                return
            }
            setTimeout(c, 200)
        };
        c()
    })
}
async function u() {
    return await p(), new Promise((t, e) => {
        const o = setTimeout(() => {
            e(new Error("Google Picker API initialization timeout"))
        }, 15e3);
        gapi.load("picker", () => {
            a = !0, clearTimeout(o), t()
        })
    })
}
async function g() {
    try {
        const t = await fetch("/api/2/googledrive_picker/token", {
            method: "GET",
            credentials: "include"
        });
        if (!t.ok) throw new Error(`Failed to get access token: ${t.status}`);
        const e = await t.json();
        if (!e.access_token) throw new Error("No access token in server response");
        return e
    } catch (t) {
        throw t
    }
}
async function w() {
    if (!a) throw new Error("Google Picker API not loaded");
    const t = await g();
    let e = t.access_token || t;
    if (typeof e == "string" && e.startsWith("{")) try {
        const o = JSON.parse(e);
        o.access_token && (e = o.access_token)
    } catch (o) {
        console.warn("Failed to parse access token JSON:", o)
    }
    return new Promise((o, r) => {
        if (typeof google > "u" || !google.picker) {
            r(new Error("Google Picker API not available - google.picker is undefined"));
            return
        }
        try {
            const i = new google.picker.DocsView(google.picker.ViewId.DOCS).setIncludeFolders(!1).setSelectFolderEnabled(!1).setMode(google.picker.DocsViewMode.LIST).setQuery('owner = "me"').setMimeTypes("text/plain,text/html,text/markdown"),
                c = "775813004843",
                l = null;
            new google.picker.PickerBuilder().enableFeature(google.picker.Feature.MULTISELECT_ENABLED).setAppId(c).setOAuthToken(e).addView(i).setCallback(n => {
                if (n[google.picker.Response.ACTION] == google.picker.Action.PICKED) {
                    const s = n[google.picker.Response.DOCUMENTS];
                    o(s)
                } else if (n[google.picker.Response.ACTION] == google.picker.Action.CANCEL) o(null);
                else if (n[google.picker.Response.ACTION] != google.picker.Action.LOADED) {
                    const s = n[google.picker.Response.ACTION];
                    (s === "error" || s === google.picker.Action.ERROR) && r(new Error("File picker encountered an authentication error"))
                }
            }).setTitle("Select files to open in Writebox").build().setVisible(!0)
        } catch (i) {
            r(i)
        }
    })
}
async function f(t) {
    try {
        const e = await fetch(`/api/2/googledrive_picker/file/text?q=${encodeURIComponent(t.id)}`, {
            method: "GET",
            credentials: "include"
        });
        if (!e.ok) throw new Error(`Failed to download file: ${e.status}`);
        const o = await e.json();
        if (!o.result || !o.result.text) throw new Error("No file content in server response");
        return o.result.text
    } catch (e) {
        throw e
    }
}
export {
    f as downloadFileContentServerAuth, u as initializeGooglePickerServerAuth, w as showFilePickerServerAuth
};