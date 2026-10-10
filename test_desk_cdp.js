const { spawn } = require('child_process');
const fs = require('fs');

async function main() {
    const edgePath = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe";
    const userDataDir = "C:\\Users\\User\\.gemini\\antigravity-ide\\brain\\c4b6aae3-72d7-4a6e-af87-08ef3c3a449e\\edge_temp_white";
    const port = 9222;

    const edgeProc = spawn(edgePath, [
        '--headless=new',
        `--remote-debugging-port=${port}`,
        `--user-data-dir=${userDataDir}`,
        '--window-size=1440,900',
        '--disable-gpu',
        'about:blank'
    ]);

    let pages = null;
    for (let i = 0; i < 15; i++) {
        await new Promise(r => setTimeout(r, 400));
        try {
            const versionRes = await fetch(`http://127.0.0.1:${port}/json/list`);
            pages = await versionRes.json();
            if (pages && pages.length > 0) break;
        } catch(e) {}
    }

    if (!pages || !pages.length) {
        console.error('Could not connect to Edge DevTools');
        edgeProc.kill();
        return;
    }

    try {
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

        // Route to Selling
        console.log('Routing to Selling workspace...');
        await send('Runtime.evaluate', {
            expression: `frappe.set_route('selling');`
        });
        await new Promise(r => setTimeout(r, 3500));

        // Click toggle to ensure it is in expanded state if collapsed
        await send('Runtime.evaluate', {
            expression: `
                const container = document.querySelector('.body-sidebar-container');
                if (container && !container.classList.contains('expanded')) {
                    const btn = document.querySelector('.ocm-sidebar-logo') || document.querySelector('.sidebar-header');
                    if (btn) btn.click();
                }
            `
        });
        await new Promise(r => setTimeout(r, 800));

        console.log('Taking screenshot 1 (White Sidebar Expanded)...');
        const snap1 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('e:\\erpnext\\desk_white_expanded.png', Buffer.from(snap1.data, 'base64'));
        console.log('Saved desk_white_expanded.png!');

        // Now toggle to collapsed
        console.log('Clicking to collapse sidebar...');
        await send('Runtime.evaluate', {
            expression: `
                const btn = document.querySelector('.ocm-header-toggle-btn') || document.querySelector('.ocm-sidebar-logo') || document.querySelector('.sidebar-header');
                if (btn) btn.click();
            `
        });
        await new Promise(r => setTimeout(r, 800));

        console.log('Taking screenshot 2 (White Sidebar Collapsed)...');
        const snap2 = await send('Page.captureScreenshot', { format: 'png' });
        fs.writeFileSync('e:\\erpnext\\desk_white_collapsed.png', Buffer.from(snap2.data, 'base64'));
        console.log('Saved desk_white_collapsed.png!');

        ws.close();
    } catch(err) {
        console.error(err);
    } finally {
        edgeProc.kill();
    }
}

main();
