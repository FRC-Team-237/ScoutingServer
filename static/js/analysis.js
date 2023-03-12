let currentTeam = null;
let currentPeriod = null;

let currentData = [];
let teams = {};

const rows = ["low", "mid", "top"];

const printScoreMatrix = matrix => {
	console.log(`Low: ${matrix["low"]}`);
	console.log(`Mid: ${matrix["mid"]}`);
	console.log(`Top: ${matrix["top"]}`);
};

const printTeamData = team => {
	console.log(`[==${team}==]`);
	teams[team].forEach(matrix => {
		printScoreMatrix(matrix);
		console.log(`-`);
	});
};

const proportionMap = (team, period = "both") => {
	const proportionMatrix = {
		"low": [...Array(9)].map(_ => { return { cube: 0, cone: 0 } }),
		"mid": [...Array(9)].map(_ => { return { cube: 0, cone: 0 } }),
		"top": [...Array(9)].map(_ => { return { cube: 0, cone: 0 } })
	};
	teams[team].forEach(matrix => {
		["low", "mid", "top"].forEach(row => {
			[...Array(9)].map((cell, index) => {
				const rawScore = matrix[row][index];

				if(period == "auto" || period == "both") {
					if(rawScore == -1) proportionMatrix[row][index].cube++;
					if(rawScore == -2) proportionMatrix[row][index].cone++;
				}
				if(period == "teleop" || period == "both") {
					if(rawScore == 1) proportionMatrix[row][index].cube++;
					if(rawScore == 2) proportionMatrix[row][index].cone++;
				}
			});
		});
	});
	return proportionMatrix;
};

const PrepData = () => {
	teams = {};
	for(let i = 0; i < currentData.length; i += 3) {
		if(teams[currentData[i].team_number] == null) {
			teams[currentData[i].team_number] = [];
		}

		const matchItem = {
			"top": [...Array(9)].map((_, x) => currentData[i+0][`row_position_${x+1}`]),
			"mid": [...Array(9)].map((_, x) => currentData[i+1][`row_position_${x+1}`]),
			"low": [...Array(9)].map((_, x) => currentData[i+2][`row_position_${x+1}`]),
		};
		teams[currentData[i].team_number].push(matchItem);
	}
};

const WriteRawCellData = () => {
	const aggregate = proportionMap(currentTeam, currentPeriod);
	rows.forEach(row => {
		for(let i = 0; i < 9; i++) {
			const cellData = aggregate[row][i];
			const cell = document.getElementById(`score${row}${i}`);
			// cell.innerText = `cube: ${cellData.cube}\ncone: ${cellData.cone}`;
			cell.innerText = `${Math.max(cellData.cube, cellData.cone)}`;
		}
	});
}

const ApplyHeatmap = () => {
	const aggregate = proportionMap(currentTeam, currentPeriod);
	// const maxCount = [...aggregate.low.flatMap(i => [i.cube, i.cone]), ...aggregate.mid.flatMap(i => [i.cube, i.cone]), ...aggregate.top.flatMap(i => [i.cube, i.cone])];
	const allValues = rows.map(row => aggregate[row].flatMap(i => [i.cube, i.cone])).flat();
	const maxCount = Math.max(...allValues);
	const minCount = Math.min(...allValues);
	const stepCount = maxCount - minCount + 1;

	const scaleRow = document.getElementById("scale-table-row");
	
	while(scaleRow.childElementCount > 0) {
		scaleRow.removeChild(scaleRow.firstElementChild);
	}

	for(let i = 0; i < stepCount; i++) {
		const scaleCell = document.createElement("td");
		scaleCell.innerText = `${i}`;
		const darkness = 1.0 - (i + 1.0) / stepCount;
		if(darkness <= 0.5) {
			scaleCell.style.color = "white";
		}
		scaleCell.style.backgroundColor = `rgb(${darkness * 255}, ${darkness * 255}, ${darkness * 255})`;
		scaleRow.appendChild(scaleCell);
	}

	rows.forEach(row => {
		for(let i = 0; i < 9; i++) {
			const cellData = aggregate[row][i];
			const cell = document.getElementById(`score${row}${i}`);
			const darkness = 1.0 - (Math.max(cellData.cube, cellData.cone) + 1.0) / stepCount;
			if(darkness <= 0.5) {
				cell.style.color = "white";
			}
			cell.style.backgroundColor = `rgb(${darkness * 255}, ${darkness * 255}, ${darkness * 255})`;
		}
	});
	WriteRawCellData();
};

const InitializeData = file => {
	const teamSelect = document.getElementById("team-select");
	const periodSelect = document.getElementById("period-select");

	while(teamSelect.childElementCount > 0) {
		teamSelect.removeChild(teamSelect.firstElementChild);
	}
	
	document.getElementById("file-response-text").innerText = `Loaded data file: ${file.name}`;
	const dataFile = file;
	try {
		currentData = JSON.parse(dataFile);
	} catch(e) {
		document.getElementById("file-response-text").innerText = `Invalid object format.`;
	}
	
	let teamList = new Set();			

	currentData.forEach(match => {
		teamList.add(match.team_number);
	});
	teamList = [...teamList].sort((a, b) => a - b);

	teamList.forEach(team => {
		const newTeamOption = document.createElement("option");
		newTeamOption.innerText = team;
		teamSelect.appendChild(newTeamOption);
	});

	PrepData();

	teamSelect.addEventListener("change", () => {
		currentTeam = teamSelect.value;
		ApplyHeatmap();
	});
	periodSelect.addEventListener("change", () => {
		currentPeriod = periodSelect.value;
		ApplyHeatmap();
	});
	
	currentPeriod = periodSelect.value;
	currentTeam = teamList[0];
	ApplyHeatmap();
}

const Initialize = () => {
	const fileUpload = document.getElementById("scouting-data-upload");

	fileUpload.addEventListener("change", e => {
		const file = fileUpload.files[0];
		const reader = new FileReader();
		reader.readAsText(file);

		reader.onerror = () => { document.getElementById("file-response-text").innerText = reader.result; };

		reader.onload = () => {
			InitializeData(reader.result);
		};
	});

	InitializeData(JSON.stringify(imported_data));
};

// const Initialize = () => {
// 	const fileUpload = document.getElementById("scouting-data-upload");

// 	fileUpload.addEventListener("change", e => {
// 		const file = fileUpload.files[0];
// 		const reader = new FileReader();
// 		reader.readAsText(file);

// 		const teamSelect = document.getElementById("team-select");
// 		const periodSelect = document.getElementById("period-select");

// 		while(teamSelect.childElementCount > 0) {
// 			teamSelect.removeChild(teamSelect.firstElementChild);
// 		}

// 		reader.onerror = () => { document.getElementById("file-response-text").innerText = reader.result; };

// 		reader.onload = () => {
// 			document.getElementById("file-response-text").innerText = `Loaded data file: ${file.name}`;
// 			const dataFile = reader.result;
// 			try {
// 				currentData = JSON.parse(dataFile);
// 			} catch(e) {
// 				document.getElementById("file-response-text").innerText = `Invalid object format.`;
// 			}
			
// 			let teamList = new Set();			

// 			currentData.forEach(match => {
// 				teamList.add(match.team_number);
// 			});
// 			teamList = [...teamList].sort((a, b) => a - b);

// 			teamList.forEach(team => {
// 				const newTeamOption = document.createElement("option");
// 				newTeamOption.innerText = team;
// 				teamSelect.appendChild(newTeamOption);
// 			});

// 			PrepData();

// 			teamSelect.addEventListener("change", () => {
// 				currentTeam = teamSelect.value;
// 				ApplyHeatmap();
// 			});
// 			periodSelect.addEventListener("change", () => {
// 				currentPeriod = periodSelect.value;
// 				ApplyHeatmap();
// 			});
			
// 			currentPeriod = periodSelect.value;
// 			currentTeam = teamList[0];
// 			ApplyHeatmap();
// 		};
// 	});
// };

window.addEventListener("DOMContentLoaded", Initialize);