const { spawn } = require('child_process');
const fs = require('fs');

async function main() {
    const edgePath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
    const userDataDir = "C:\\Users\\User\\.gemini\\antigravity-ide\\brain\\c4b6aae3-72d7-4a6e-af87-08ef3c3a449e\\edge_temp";
    
    const edgeProc = spawn(edgePath, [
        '--headless=new',
        '--remote-debugging-port=9222',
        `--user-data-dir=${userDataDir}`,
        '--window-size=1440,900',
        '--disable-gpu',
        'about:blank'
    ]);

    await new Promise(r => setTimeout(r, 1200));

    try {
        const versionRes = await fetch('http://127.0.0.1:9222/json/list');
        const pages = await versionRes.json();
        const wsUrl = pages[0].webSocketDebuggerUrl;

        const ws = new WebSocket(wsUrl);
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

        const cookiesTxt = fs.readFileSync('cookies.txt', 'utf8');
        const sidMatch = cookiesTxt.match(/sid\s+([a-f0-9]+)/);
        const sid = sidMatch ? sidMatch[1] : '';

        await send('Network.setCookie', {
            name: 'sid',
            value: sid,
            domain: 'localhost',
            path: '/',
            httpOnly: true
        });

        console.log('Navigating to http://localhost:8080/app...');
        await send('Page.navigate', { url: 'http://localhost:8080/app' });

        await new Promise(r => setTimeout(r, 4000));

        // Now set route to Selling via frappe.set_route
        console.log('Routing to Selling workspace...');
        await send('Runtime.evaluate', {
            expression: `frappe.set_route('selling');`
        });

        await new Promise(r => setTimeout(r, 3000));

        console.log('Taking screenshot 1 (Workspace Expanded)...');
        const snap1 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('e:\\erpnext\\workspace_expanded.png', Buffer.from(snap1.data, 'base64'));
        console.log('workspace_expanded.png saved!');

        const info1 = await send('Runtime.evaluate', {
            expression: `({
                route: frappe.get_route(),
                sidebarExists: !!document.querySelector('.body-sidebar'),
                sidebarVisible: document.querySelector('.body-sidebar')?.offsetParent !== null,
                sidebarContainerClass: document.querySelector('.body-sidebar-container')?.className,
                sidebarWidth: document.querySelector('.body-sidebar')?.offsetWidth,
                placeholderWidth: document.querySelector('.body-sidebar-placeholder')?.offsetWidth,
                hasExpandedClass: document.querySelector('.body-sidebar-container')?.classList.contains('expanded'),
                itemsCount: document.querySelectorAll('.standard-sidebar-item').length
            })`,
            returnByValue: true
        });
        console.log('Workspace Expanded Info:', info1.result.value);

        // Click the sidebar header logo to toggle/collapse
        console.log('Clicking sidebar header logo to collapse...');
        await send('Runtime.evaluate', {
            expression: `
                const logo = document.querySelector('.ocm-sidebar-logo');
                if (logo) {
                    logo.click();
                } else {
                    document.querySelector('.sidebar-header').click();
                }
            `
        });

        await new Promise(r => setTimeout(r, 800));

        console.log('Taking screenshot 2 (Workspace Collapsed)...');
        const snap2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('e:\\erpnext\\workspace_collapsed.png', Buffer.from(snap2.data, 'base64'));
        console.log('workspace_collapsed.png saved!');

        const info2 = await send('Runtime.evaluate', {
            expression: `({
                sidebarContainerClass: document.querySelector('.body-sidebar-container')?.className,
                sidebarWidth: document.querySelector('.body-sidebar')?.offsetWidth,
                placeholderWidth: document.querySelector('.body-sidebar-placeholder')?.offsetWidth,
                bodyClasses: document.body.className
            })`,
            returnByValue: true
        });
        console.log('Workspace Collapsed Info:', info2.result.value);

        // Click the sidebar header again to expand back
        console.log('Clicking sidebar header again to expand...');
        await send('Runtime.evaluate', {
            expression: `
                document.querySelector('.sidebar-header').click();
            `
        });

        await new Promise(r => setTimeout(r, 800));

        console.log('Taking screenshot 3 (Workspace Expanded Again)...');
        const snap3 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('e:\\erpnext\\workspace_expanded_again.png', Buffer.from(snap3.data, 'base64'));
        console.log('workspace_expanded_again.png saved!');

        ws.close();
    } catch (e) {
        console.error('Error:', e);
    } finally {
        edgeProc.kill();
    }
}

main();
