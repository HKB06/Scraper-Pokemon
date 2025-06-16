import React, { useEffect, useState } from "react";

function App() {
  const [cards, setCards] = useState([]);
  const [search, setSearch] = useState("");
  const [author, setAuthor] = useState("");
  const [serie, setSerie] = useState("");
  const [filtered, setFiltered] = useState([]);

  useEffect(() => {
    fetch("/cards.json")
      .then((res) => res.json())
      .then((data) => setCards(data));
  }, []);

  useEffect(() => {
    setFiltered(
      cards.filter(
        (card) =>
          card.nom.toLowerCase().includes(search.toLowerCase()) &&
          card.illustrateur.toLowerCase().includes(author.toLowerCase()) &&
          card.serie.toLowerCase().includes(serie.toLowerCase())
      )
    );
  }, [cards, search, author, serie]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-100 via-red-100 to-blue-100 p-8">
      <h1 className="text-4xl font-extrabold text-center mb-8 flex items-center justify-center gap-4" style={{ fontFamily: "'Press Start 2P', cursive" }}>
        <span role="img" aria-label="pokeball">🕹️</span>
        Recherche de cartes Pokémon
        <span role="img" aria-label="pokeball">⚡</span>
      </h1>
      <div className="flex flex-col md:flex-row gap-4 justify-center mb-8">
        <input
          className="p-2 rounded border-2 border-yellow-400 shadow focus:outline-none focus:ring-2 focus:ring-red-400"
          type="text"
          placeholder="Nom de la carte"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <input
          className="p-2 rounded border-2 border-blue-400 shadow focus:outline-none focus:ring-2 focus:ring-yellow-400"
          type="text"
          placeholder="Nom de l'illustrateur"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
        />
        <input
          className="p-2 rounded border-2 border-red-400 shadow focus:outline-none focus:ring-2 focus:ring-blue-400"
          type="text"
          placeholder="Série"
          value={serie}
          onChange={(e) => setSerie(e.target.value)}
        />
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {filtered.map((card, idx) => (
          <div
            key={idx}
            className="bg-white rounded-xl shadow-lg p-4 flex flex-col items-center border-4 border-yellow-200 hover:border-red-400 transition-all duration-200 hover:scale-105"
          >
            <div className="font-extrabold text-xl mb-2 text-red-500">{card.nom}</div>
            <div className="text-blue-600 mb-1 font-semibold">Série : {card.serie}</div>
            <div className="text-gray-500 text-sm italic">Illustrateur : {card.illustrateur}</div>
            <div className="mt-2 text-2xl">⭐</div>
          </div>
        ))}
      </div>
      {filtered.length === 0 && (
        <div className="text-center text-gray-500 mt-8">Aucune carte trouvée.</div>
      )}
      <footer className="mt-12 text-center text-xs text-gray-400">
        Fait avec <span role="img" aria-label="pokeball">❤️</span> par un dresseur Hugo
      </footer>
    </div>
  );
}

export default App;