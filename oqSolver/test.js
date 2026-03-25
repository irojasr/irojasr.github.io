const fs = require('fs');

function getCombinations(arr, k) {
    const results = [];
    function helper(start, combo) {
        if (combo.length === k) {
            results.push([...combo]);
            return;
        }
        const remaining = k - combo.length;
        for (let i = start; i <= arr.length - remaining; i++) {
            combo.push(arr[i]);
            helper(i + 1, combo);
            combo.pop();
        }
    }
    helper(0, []);
    return results;
}

function getAdjCount(board, r, c) {
    let count = 0;
    for (const tIndex of board) {
        const tr = Math.floor(tIndex / 5);
        const tc = tIndex % 5;
        if (Math.max(Math.abs(tr - r), Math.abs(tc - c)) <= 1 && tIndex !== (r * 5 + c)) {
            count++;
        }
    }
    return count;
}

const allBoards = getCombinations(Array.from({length: 25}, (_,i)=>i), 4);
let tileState = Array(25).fill(null);

tileState[1 * 5 + 3] = 2; // (1,3) = 2
tileState[1 * 5 + 2] = 1; // (1,2) = 1
tileState[1 * 5 + 4] = 1; // (1,4) = 1
tileState[2 * 5 + 2] = 0; // (2,2) = 0
tileState[0 * 5 + 2] = 'T'; // (0,2) = T
tileState[2 * 5 + 4] = 'T'; // (2,4) = T

const validBoards = allBoards.filter(board => {
    for (let i = 0; i < 25; i++) {
        const state = tileState[i];
        if (state === null) continue;

        if (state === 'T' || state === 'R') {
            if (!board.includes(i)) return false;
        } else {
            if (board.includes(i)) return false;
            const r = Math.floor(i / 5);
            const c = i % 5;
            if (getAdjCount(board, r, c) !== state) return false;
        }
    }
    return true;
});

console.log("Valid boards:", validBoards.length);

function score(B) {
    console.log("\\n--- SCORING WITH B =", B, "---");
    let pointsMapping = [10+B, 20+B, 35+B, 55+B, 90+B];
    let targetPts = 5+B; // since tsFound = 2
    let best = {name: "", exp: -1, p: -1};

    for(let i=0; i<25; i++){
        if(tileState[i] !== null) continue;
        let tCount = 0;
        let pSum = 0;
        for(let b of validBoards){
            if(b.includes(i)) tCount++;
            else {
                pSum += pointsMapping[getAdjCount(b, Math.floor(i/5), i%5)];
            }
        }
        let probT = tCount / validBoards.length;
        let expMoves = Math.max(0.0001, 1 - probT);
        let eff = ((probT * targetPts) + (pSum / validBoards.length)) / expMoves;
        
        const loc = `(${Math.floor(i/5)+1}, ${(i%5)+1})`;
        if(loc === "(4, 5)" || loc === "(4, 1)" || loc === "(5, 2)" || loc === "(5, 4)") {
            console.log(`Tile ${loc}: P(T)=${(probT*100).toFixed(1)}%, Efficiency=${eff.toFixed(2)}`);
        }
        if(eff > best.exp) {
            best = {name: loc, exp: eff, p: probT};
        }
    }
    console.log("BEST OVERALL:", best.name, "with Eff", best.exp.toFixed(2));
}

score(0);
score(100);
score(10000);
