const translations = {
    en: {


        titel1: "Unlimited films, TV programmes and more.",
        titel2: "Watch anywhere. Cancel at any time.",
        titel3: "Ready to watch? Enter your email to create or restart your membership.",
        mail: "Email address",
        start: "Get Started >",
        signin: "Sign in",
        section11: "Enjoy on your TV.",
        section12: "Watch on smart TVs, PlayStation, Xbox, Chromecast, Apple TV, Blu-ray players and more.",
        section21: "Download your programmes to watch offline.",
        section22: "Save your favourites easily and always have something to watch.",
        section31: "Watch everywhere.",
        section32: "Stream unlimited movies and TV shows on your phone, tablet, laptop, and TV.",
        section41: "Create profiles for kids.",
        section42: "Send kids on adventures with their favorite characters in a space made just for them — free with your membership.",
        questions: "Frequently Asked Questions",
        start2: "Get STarted >",
        prompt2: "Ready to watch? Enter your email to create or restart your membership.",

    },
    fr: {

        titel1: "Films et séries en illimité, et bien plus",
        titel2: "Regardez où que vous soyez. Annulez à tout moment.",
        titel3: "Prêt à regarder ? Entrez votre email pour créer ou redémarrer votre adhésion.",
        mail: "Adresse e-mail",
        start: "Commencer >",
        signin: "S'identifier",
        section11: "Profitez-en sur votre télévision.",
        section12: "Regardez sur des smart TV, PlayStation, Xbox, Chromecast, Apple TV, lecteurs Blu-ray et plus encore.",
        section21: "Téléchargez vos programmes pour les regarder hors ligne.",
        section22: "Sauvegardez facilement vos favoris et ayez toujours quelque chose à regarder.",
        section31: "Regardez partout.",
        section32: "Regardez des films et des émissions de télévision en illimité sur votre téléphone, votre tablette, votre ordinateur portable et votre téléviseur.",
        section41: "Créez des profils pour les enfants.",
        section42: "Envoyez vos enfants à l'aventure avec leurs personnages préférés dans un espace conçu spécialement pour eux, gratuitement avec votre abonnement.",
        questions: "Questions Fréquemment Posées",
        start2: "Commencer >",
        prompt2: "Prêt à regarder ? Entrez votre email pour créer ou redémarrer votre adhésion.",

    },
    ndls: {

        titel1: "Onbeperkt series, films en nog veel meer kijken",
        titel2: "Kijk overal. Annuleer op elk gewenst moment.",
        titel3: "Klaar om te kijken? Voer uw e-mailadres in om uw lidmaatschap aan te maken of opnieuw te starten.",
        mail: "E-mailadres",
        start: "Aan de slag >",
        signin: "Inloggen",
        section11: "Geniet ervan op uw TV.",
        section12: "Bekijk op smart-TV's, PlayStation, Xbox, Chromecast, Apple TV, Blu-ray-spelers en meer.",
        section21: "Download uw programma's om ze offline te bekijken.",
        section22: "Sla uw favorieten eenvoudig op, zodat u altijd iets te kijken heeft.",
        section31: "Kijk overal.",
        section32: "Stream onbeperkt films en TV-programma's op uw telefoon, tablet, laptop en TV.",
        section41: "Maak profielen voor kinderen.",
        section42: "Stuur kinderen op avontuur met hun favoriete personages in een ruimte die speciaal voor hen is gemaakt — gratis bij je lidmaatschap.",
        questions: "Veelgestelde Vragen",
        start2: "Aan de slag",
        prompt2: "Klaar om te kijken? Voer uw e-mailadres in om uw lidmaatschap aan te maken of opnieuw te starten.",

    },

};

document.getElementById("language-select").addEventListener("change", function() {
    const selectedLanguage = this.value;
    updateText(selectedLanguage);
});

function updateText(language) {
    const elements = document.querySelectorAll("[data-text]");
    elements.forEach((element) => {
        const textKey = element.getAttribute("data-text");
        element.textContent = translations[language][textKey];
    });
}
