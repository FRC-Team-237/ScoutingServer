const rowNames = ["low", "mid", "high"];
const valueNames = ["none", "cube", "cone"];
const valueStrings = [".", "◼", "▲"];
const objectColors = ["#00000000", "#9922cc", "#ee9922"];

const scoreValues = {
	high: [],
	mid: [],
	low: []
};

const scoreButtons = {
	high: [],
	mid: [],
	low: []
};

const SetItem = (row, index, value) => {
	if(!["low", "mid", "high"].includes(row)) return;
	if(!(Number.isInteger(index) && 0 <= index && index <= 8)) return;
	if(!(Number.isInteger(value) && 0 <= value && value <= 2)) value = 0;

	scoreValues[row][index] = value;
	scoreValues[row][index] %= 3;
	UpdateButton(row, index);
};

const CycleItem = (row, index) => {
	SetItem(row, index, (scoreValues[row][index] + 1) % 3);

	const scoreType = scoreButtons[row][index].dataset.scoretype;
	if(!scoreType.includes("cube") && scoreValues[row][index] == 1) SetItem(row, index, scoreValues[row][index] + 1);
	if(!scoreType.includes("cone") && scoreValues[row][index] == 2) SetItem(row, index, scoreValues[row][index] + 1);

	SetItem(row, index, scoreValues[row][index] % 3);

	UpdateButton(row, index);
}

const UpdateButton = (row, index) => {
	const scoreValue = scoreValues[row][index];
	scoreButtons[row][index].style.color = objectColors[scoreValue];
	scoreButtons[row][index].dataset.score = valueNames[scoreValue];
	UpdateJSONPreview();
};

const Init = () => {
	scoreButtons.high = document.querySelectorAll("td[name^='scorehigh']");
	scoreButtons.mid = document.querySelectorAll("td[name^='scoremid']");
	scoreButtons.low = document.querySelectorAll("td[name^='scorelow']");

	rowNames.forEach(row => {
		for(let i = 0; i < 9; i++) {
			scoreButtons[row][i].addEventListener('click', () => { CycleItem(row, i); });
			scoreButtons[row][i].clientHeight = scoreButtons[row][i].clientWidth;
			SetItem(row, i, 0);
		}
	});

	document.querySelector("button[data-target='confirm-submit-panel'").addEventListener('click', TrySubmit);
	document.getElementById("match-result-form").addEventListener('change', UpdateJSONPreview);
	document.getElementById("submit-results").addEventListener('click', () => {

		const xhr = new XMLHttpRequest();
		xhr.open("POST", "/matches");
		xhr.setRequestHeader("Accept", "application/json");
		xhr.setRequestHeader("Content-Type", "application/json");

		xhr.onreadystatechange = () => {
			if(xhr.readyState === 4) {
				console.log(xhr.status);
				console.log(xhr.responseText);
			}
		};

		xhr.send(JSON.stringify(ResultsToObject()));

		window.scrollTo(0, 0);
		document.getElementById("match-result-form").reset();
	});
};

const UpdateJSONPreview = () => {
	(document.getElementById("json-preview") || []).innerText = JSON.stringify(ResultsToObject(),
		(k, v) => {
			if(v instanceof Array)
				return JSON.stringify(v);
			return v;
		}, "\t");
}

const ResultsToObject = () => {
	let result = {
		matchNumber: 0,
		teamNumber: 0,
		alliance: "",
		autonomous: { mobility: false, charge: 0 },
		endgame: { charge: 0 },
		win: false,
		notes: "",
		scoreMatrix: { high: [], mid: [], low: [] }
	}

	result.matchNumber = document.getElementById("match-number").value;
	result.teamNumber = document.getElementById("team-number").value;
	result.alliance = document.getElementById("alliance-color").checked ? "blue" : "red";
	result.autonomous.mobility = document.getElementById("mobility").checked;

	const chargeSuffixes = ["none", "docked", "engaged"];
	
	const autoCharge = document.querySelector('input[name="charge-status-auto"]:checked').id;
	result.autonomous.charge = chargeSuffixes.findIndex(c => autoCharge.includes(c));
	
	const endCharge = document.querySelector('input[name="charge-status-end"]:checked').id;
	result.endgame.charge = chargeSuffixes.findIndex(c => endCharge.includes(c));

	result.win = document.getElementById("win-status").checked;
	result.notes = document.getElementById("notes-field").value;
	result.scoreMatrix = scoreValues;
	return result;
}

const TrySubmit = () => {
	const formErrors = document.getElementById("form-errors");
	while(formErrors.hasChildNodes()) formErrors.removeChild(formErrors.childNodes[0]);

	document.querySelectorAll("input:invalid").forEach(input => {
		const newError = document.createElement("blockquote");
		const errorTitle = document.createElement("h5");
		errorTitle.className = "title is-5 has-text-danger";
		errorTitle.innerText = document.getElementById(input.id + "-label").innerText;

		const errorBody = document.createElement("p");
		errorBody.className = "subtitle is-6";
		errorBody.innerText = input.validationMessage;
		
		newError.appendChild(errorTitle);
		newError.appendChild(errorBody);

		formErrors.appendChild(newError);
	});

	document.getElementById("submit-results").disabled = formErrors.hasChildNodes();
};

document.addEventListener('DOMContentLoaded', () => {
	// Functions to open and close a modal
	const openModal = $el => $el.classList.add('is-active');
	const closeModal = $el => $el.classList.remove('is-active');

	const closeAllModals = () => (document.querySelectorAll('.modal') || []).forEach($modal => closeModal($modal));

	(document.querySelectorAll('.js-modal-trigger') || []).forEach($trigger => {
		const modal = $trigger.dataset.target;
		const $target = document.getElementById(modal);

		$trigger.addEventListener('click', () => openModal($target) );
	});

	// Add a click event on various child elements to close the parent modal
	(document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach($close => {
		const $target = $close.closest('.modal');

		$close.addEventListener('click', () => closeModal($target) );
	});

	// Add a keyboard event to close all modals
	document.addEventListener('keydown', event => {
		const e = event || window.event;

		if (e.key === "Escape") 
			closeAllModals();
	});
});

window.onbeforeunload = () => "";