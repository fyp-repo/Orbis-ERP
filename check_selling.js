const fs = require('fs');
const { spawn } = require('child_process');

(async () => {
    const edgePath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
    const userDataDir = 'C:\\Users\\User\\.gemini\\antigravity-ide\\brain\\c4b6aae3-72d7-4a6e-af87-08ef3c3a449e\\edge_temp2';
    const edgeProc = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=9223',
        '--user-data-dir=' + userDataDir,
        '--window-size=1440,900',
        '--disable-gpu',
        'about:blank'
    ]);
    await new Promise(r => setTimeout(r, 1200));
    try {
        const versionRes = await fetch('http://127.0.0.1:9223/json/list');
        const pages = await versionRes.json();
        const ws = new WebSocket(pages[0].webSocketDebuggerUrl);
        await new Promise((resolve) => ws.onopen = resolve);
        let id = 1;
        const pending = new Map();
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.id && pending.has(data.id)) {
                const resolve = pending.get(data.id);
                pending.delete(data.id);
                resolve(data.result);
            }
        };
        const send = (method, params = {}) => new Promise((resolve) => {
            const curId = id++;
            pending.set(curId, resolve);
            ws.send(JSON.stringify({ id: curId, method, params }));
        });
        await send('Network.enable');
        await send('Page.enable');
        const sid = fs.readFileSync('cookies.txt', 'utf8').match(/sid\s+([a-f0-9]+)/)[1];
        await send('Network.setCookie', { name: 'sid', value: sid, domain: 'localhost', path: '/', httpOnly: true });
        
        console.log('Navigating to http://localhost:8080/app/selling...');
        await send('Page.navigate', { url: 'http://localhost:8080/app/selling' });
        await new Promise(r => setTimeout(r, 6000));
        
        const snap = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('e:\\erpnext\\selling_workspace.png', Buffer.from(snap.data, 'base64'));
        
        const domInfo = await send('Runtime.evaluate', {
            expression: `JSON.stringify({
                route: window.frappe ? frappe.get_route() : null,
                sidebarExists: !!document.querySelector('.body-sidebar'),
                sidebarContainerClass: document.querySelector('.body-sidebar-container')?.className,
                placeholderWidth: document.querySelector('.body-sidebar-placeholder')?.offsetWidth,
                sidebarWidth: document.querySelector('.body-sidebar')?.offsetWidth,
                headerSubtitle: document.querySelector('.header-subtitle')?.textContent,
                sidebarItems: document.querySelectorAll('.standard-sidebar-item').length
            })`
        });
        console.log('Selling page info:', domInfo.result.value);

        // Now test collapse click
        console.log('Testing collapse click...');
        await send('Runtime.evaluate', {
            expression: `
                // Click the sidebar header icon or toggle
                const header = document.querySelector('.sidebar-header');
                const logo = document.querySelector('.ocm-sidebar-logo');
                if (logo) logo.click();
                else if (header) header.click();
            `
        });

        await new Promise(r => setTimeout(r, 800));

        const snapCollapsed = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('e:\\erpnext\\selling_collapsed.png', Buffer.from(snapCollapsed.data, 'base64'));

        const domInfoCollapsed = await send('Runtime.evaluate', {
            expression: `JSON.stringify({
                sidebarContainerClass: document.querySelector('.body-sidebar-container')?.className,
                sidebarWidth: document.querySelector('.body-sidebar')?.offsetWidth,
                hasCollapsedClass: document.body.classList.contains('ocm-sidebar-collapsed')
            })`
        });
        console.log('Collapsed page info:', domInfoCollapsed.result.value);

        ws.close();
    } catch(err) {
        console.error(err);
    } finally {
        edgeProc.kill();
    }
})();
