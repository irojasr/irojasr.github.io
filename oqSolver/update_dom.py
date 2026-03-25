import codecs

file_path = r"j:\irojasr.github.io\oqSolver\index.html"

with codecs.open(file_path, "r", "utf-8") as f:
    html = f.read()

# 1. Replace CSS
css_old = """        .keypad-wrapper {
            position: fixed;
            bottom: -300px;
            left: 0;
            width: 100%;
            background: rgba(15, 17, 26, 0.95);
            backdrop-filter: blur(20px);
            border-top: 1px solid var(--border-color);
            transition: bottom 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            padding: 20px;
            z-index: 100;
            box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
        }

        .keypad-wrapper.visible {
            bottom: 0;
        }

        .keypad {
            width: 100%;
            max-width: 500px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
        }

        .keypad-title {
            grid-column: 1 / -1;
            text-align: center;
            margin-bottom: 10px;
            font-weight: 600;
            color: var(--text-muted);
        }

        .key-btn {
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 15px 0;
            border-radius: 10px;
            font-size: 1.3rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .key-btn:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: scale(1.05);
        }

        .key-btn:active {
            transform: scale(0.95);
        }

        .key-target {
            color: var(--accent-pink);
            border-color: var(--accent-pink);
        }

        .key-clear {
            grid-column: span 2;
            background: rgba(255, 68, 68, 0.1);
            border-color: rgba(255, 68, 68, 0.3);
            color: #ff4444;
        }

        .reset-btn {
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 10px;
        }

        .reset-btn:hover {
            color: var(--text-main);
            border-color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }

        #close-keypad {
            position: absolute;
            top: 15px;
            right: 20px;
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 1.5rem;
            cursor: pointer;
        }

        /* Number Colors */
        .color-0 {
            color: #6b7280;
        }

        .color-1 {
            color: #3b82f6;
        }

        .color-2 {
            color: #10b981;
        }

        .color-3 {
            color: #ef4444;
        }

        .color-4 {
            color: #a855f7;
        }"""
        
css_new = """        .reset-btn {
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 10px;
        }

        .reset-btn:hover {
            color: var(--text-main);
            border-color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }

        /* Mudae Cycle Background Colors */
        .bg-purple { background-color: #a855f7 !important; border-color: #c084fc !important; color: white !important; }
        .bg-blue   { background-color: #3b82f6 !important; border-color: #60a5fa !important; color: white !important; }
        .bg-teal   { background-color: #14b8a6 !important; border-color: #2dd4bf !important; color: white !important; }
        .bg-green  { background-color: #10b981 !important; border-color: #34d399 !important; color: white !important; }
        .bg-yellow { background-color: #eab308 !important; border-color: #facc15 !important; color: white !important; }
        .bg-orange { background-color: #f97316 !important; border-color: #fb923c !important; color: white !important; }
        .bg-red    { background-color: #ef4444 !important; border-color: #f87171 !important; color: white !important; }"""

html = html.replace(css_old, css_new)

# 2. Keypad wrapper
keypad_old = """    <div class="keypad-wrapper" id="keypadWrapper">
        <button id="close-keypad" onclick="closeKeypad()">&times;</button>
        <div class="keypad">
            <div class="keypad-title" id="keypadTitle">Select state for tile</div>
            <button class="key-btn color-0" onclick="setTileState(0)">0</button>
            <button class="key-btn color-1" onclick="setTileState(1)">1</button>
            <button class="key-btn color-2" onclick="setTileState(2)">2</button>
            <button class="key-btn color-3" onclick="setTileState(3)">3</button>
            <button class="key-btn color-4" onclick="setTileState(4)">4</button>
            <button class="key-btn key-target" onclick="setTileState('T')">🎯 T</button>
            <button class="key-btn key-clear" onclick="setTileState(null)">❌ Clear</button>
        </div>
    </div>"""

html = html.replace(keypad_old, "")

# 3. Globals update
js_globals_old = """        let probabilities = Array(25).fill(0);
        let selectedIndex = null;
        let tsFound = 0;"""
        
js_globals_new = """        let probabilities = Array(25).fill(0);
        let tsFound = 0;
        const cycleOrder = [null, 'T', 0, 1, 2, 3, 4, 'R'];"""

html = html.replace(js_globals_old, js_globals_new)

# 4. grid mapping
js_dom_old = """        const gridElement = document.getElementById('grid');
        const keypadWrapper = document.getElementById('keypadWrapper');
        const keypadTitle = document.getElementById('keypadTitle');
        const remainingText = document.getElementById('remainingText');"""

js_dom_new = """        const gridElement = document.getElementById('grid');
        const remainingText = document.getElementById('remainingText');"""

html = html.replace(js_dom_old, js_dom_new)

# 5. Onclick replace
js_onclk_old = """            tile.onclick = () => selectTile(i);"""
js_onclk_new = """            tile.onclick = () => cycleTileState(i);"""
html = html.replace(js_onclk_old, js_onclk_new)

# 6. Interaction API replace
js_api_old = """        function resetBoard() {
            tileState.fill(null);
            closeKeypad();
            updateSolver();
        }

        function selectTile(index) {
            if (selectedIndex !== null) {
                document.getElementById(`tile-${selectedIndex}`).classList.remove('selected');
            }
            selectedIndex = index;
            document.getElementById(`tile-${selectedIndex}`).classList.add('selected');

            const r = Math.floor(index / 5) + 1;
            const c = (index % 5) + 1;
            keypadTitle.textContent = `Set state for Tile [${r}, ${c}]`;
            keypadWrapper.classList.add('visible');
        }

        function closeKeypad() {
            if (selectedIndex !== null) {
                document.getElementById(`tile-${selectedIndex}`).classList.remove('selected');
                selectedIndex = null;
            }
            keypadWrapper.classList.remove('visible');
        }

        function setTileState(state) {
            if (selectedIndex === null) return;
            tileState[selectedIndex] = state;
            closeKeypad();
            updateSolver();
        }

        function updateSolver() {
            tsFound = tileState.filter(s => s === 'T').length;
            let numbersFound = tileState.filter(s => s !== null && s !== 'T').length;
            clicksLeft = 7 - numbersFound - (tsFound === 4 ? 1 : 0);"""

js_api_new = """        function resetBoard() {
            tileState.fill(null);
            updateSolver();
        }

        function cycleTileState(index) {
            const currentState = tileState[index];
            const currentIndex = cycleOrder.indexOf(currentState);
            const nextState = cycleOrder[(currentIndex + 1) % cycleOrder.length];
            tileState[index] = nextState;
            updateSolver();
        }

        function updateSolver() {
            tsFound = tileState.filter(s => s === 'T' || s === 'R').length;
            let numbersFound = tileState.filter(s => typeof s === 'number').length;
            let redFound = tileState.filter(s => s === 'R').length;
            clicksLeft = 7 - numbersFound - redFound;"""

html = html.replace(js_api_old, js_api_new)

# 7. Add Red to target arrays
js_validity_old = """                    if (state === 'T') {
                        if (!board.includes(i)) return false;
                    } else {"""
                    
js_validity_new = """                    if (state === 'T' || state === 'R') {
                        if (!board.includes(i)) return false;
                    } else {"""

html = html.replace(js_validity_old, js_validity_new)

# 8. Render Color replacement
js_render_old = """                tile.className = 'tile' + (i === selectedIndex ? ' selected' : '');

                if (state !== null) {
                    // Revealed state
                    probSpan.textContent = '';
                    if (state === 'T') {
                        valueSpan.textContent = '🎯';
                        tile.style.background = 'rgba(255, 0, 106, 0.15)';
                        tile.style.borderColor = 'var(--accent-pink)';
                        tile.style.color = '#fff';
                    } else {
                        valueSpan.textContent = state;
                        tile.style.background = '#252836';
                        tile.style.borderColor = 'rgba(255,255,255,0.05)';
                        valueSpan.className = `color-${state}`;
                    }
                } else {
                    // Unknown state
                    valueSpan.className = '';
                    valueSpan.textContent = '';"""

js_render_new = """                tile.className = 'tile';
                tile.style.background = '';
                tile.style.borderColor = '';
                tile.style.color = '';

                if (state !== null) {
                    // Revealed state
                    probSpan.textContent = '';
                    if (state === 'T') {
                        valueSpan.textContent = '🎯';
                        tile.classList.add('bg-purple');
                    } else if (state === 'R') {
                        valueSpan.textContent = '🔴';
                        tile.classList.add('bg-red');
                    } else {
                        valueSpan.textContent = state;
                        if (state === 0) tile.classList.add('bg-blue');
                        if (state === 1) tile.classList.add('bg-teal');
                        if (state === 2) tile.classList.add('bg-green');
                        if (state === 3) tile.classList.add('bg-yellow');
                        if (state === 4) tile.classList.add('bg-orange');
                    }
                } else {
                    // Unknown state
                    valueSpan.textContent = '';"""

html = html.replace(js_render_old, js_render_new)

with codecs.open(file_path, "w", "utf-8") as f:
    f.write(html)
print("Updated successfully!")
