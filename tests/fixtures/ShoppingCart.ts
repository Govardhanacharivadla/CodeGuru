// TypeScript Sample with Types
interface Product {
    id: number;
    name: string;
    price: number;
    inStock: boolean;
}

class ShoppingCart {
    private items: Product[] = [];

    addItem(product: Product): void {
        this.items.push(product);
        console.log(`Added ${product.name} to cart`);
    }

    removeItem(productId: number): boolean {
        const index = this.items.findIndex(item => item.id === productId);
        if (index !== -1) {
            this.items.splice(index, 1);
            return true;
        }
        return false;
    }

    getTotal(): number {
        return this.items.reduce((sum, item) => sum + item.price, 0);
    }

    getItems(): Product[] {
        return [...this.items];
    }
}

function calculateDiscount(price: number, discountPercent: number): number {
    return price * (1 - discountPercent / 100);
}

function isAffordable(price: number, budget: number): boolean {
    return price <= budget;
}

// Usage
const cart = new ShoppingCart();
const laptop: Product = { id: 1, name: 'Laptop', price: 999, inStock: true };
cart.addItem(laptop);
console.log(`Total: $${cart.getTotal()}`);
