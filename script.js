const BACKEND_URL = "http://localhost:3000";
const EXCHANGES = ["Binance", "OKX", "KuCoin", "Mexc"];
const CRYPTOS = ["BTC", "ETH", "BNB", "ADA", "XRP"];

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("crypto-container");

    CRYPTOS.forEach(symbol => {
        const card = document.createElement("div");
        card.classList.add("card");
        card.innerHTML = `
            <h3>${symbol}</h3>
            <button onclick="fetchOrderBook('${symbol}')">Ver Book de Ofertas</button>
        `;
        container.appendChild(card);
    });

    const modal = document.getElementById("modal");
    const closeModal = document.querySelector(".close");
    closeModal.addEventListener("click", () => modal.style.display = "none");

    document.getElementById("tab-buy").addEventListener("click", () => showOrders("buy"));
    document.getElementById("tab-sell").addEventListener("click", () => showOrders("sell"));
});

async function fetchOrderBook(symbol) {
    const modal = document.getElementById("modal");
    const modalTitle = document.getElementById("modal-title");
    const orderbookList = document.getElementById("orderbook-list");

    modalTitle.textContent = `Book de Ofertas - ${symbol}`;
    modal.style.display = "flex";
    orderbookList.innerHTML = "<li>Buscando ofertas...</li>";

    let bestBuyExchange = null;
    let bestSellExchange = null;
    let bestBuyPrice = Infinity;
    let bestSellPrice = 0;

    let orderBooks = {};

    // Buscar os books de ofertas de todas as exchanges
    for (const exchange of EXCHANGES) {
        try {
            const response = await fetch(`${BACKEND_URL}/orderbook/${exchange}/${symbol}`);
            const data = await response.json();

            if (data.buyOrders && data.sellOrders) {
                // Verifica a melhor exchange para compra (quem vende mais barato)
                const lowestSell = parseFloat(data.sellOrders[0][0]);
                if (lowestSell < bestBuyPrice) {
                    bestBuyPrice = lowestSell;
                    bestBuyExchange = exchange;
                }

                // Verifica a melhor exchange para venda (quem paga mais caro)
                const highestBuy = parseFloat(data.buyOrders[0][0]);
                if (highestBuy > bestSellPrice) {
                    bestSellPrice = highestBuy;
                    bestSellExchange = exchange;
                }

                // Guarda os dados para acesso posterior
                orderBooks[exchange] = {
                    buyOrders: data.buyOrders.map(order => ({
                        price: parseFloat(order[0]),
                        quantity: parseFloat(order[1])
                    })),
                    sellOrders: data.sellOrders.map(order => ({
                        price: parseFloat(order[0]),
                        quantity: parseFloat(order[1])
                    }))
                };
            }
        } catch (error) {
            console.error(`Erro ao buscar book de ofertas na ${exchange}:`, error);
        }
    }

    // Define qual exchange será usada em cada aba
    window.orderbookData = {
        bestBuyExchange: bestBuyExchange,
        bestSellExchange: bestSellExchange,
        orderBooks: orderBooks
    };

    showOrders("buy");
}

function showOrders(type) {
    const orderbookList = document.getElementById("orderbook-list");
    const tabBuy = document.getElementById("tab-buy");
    const tabSell = document.getElementById("tab-sell");

    tabBuy.classList.remove("active");
    tabSell.classList.remove("active");

    if (type === "buy") {
        tabBuy.classList.add("active");
    } else {
        tabSell.classList.add("active");
    }

    orderbookList.innerHTML = "";

    if (window.orderbookData) {
        const bestExchange = type === "buy" ? window.orderbookData.bestBuyExchange : window.orderbookData.bestSellExchange;
        const orders = type === "buy" ? window.orderbookData.orderBooks[bestExchange].buyOrders : window.orderbookData.orderBooks[bestExchange].sellOrders;

        if (!orders || orders.length === 0) {
            orderbookList.innerHTML = "<li>Sem ordens disponíveis</li>";
            return;
        }

        orders.forEach(order => {
            const li = document.createElement("li");
            li.classList.add(type === "buy" ? "buy" : "sell");
            li.textContent = `[${bestExchange}] Preço: $${order.price.toFixed(2)} | Quantidade: ${order.quantity.toFixed(2)}`;
            orderbookList.appendChild(li);
        });
    }
}
