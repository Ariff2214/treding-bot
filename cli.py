import argparse
from dotenv import load_dotenv
from bot.validators import validate_order_input, ValidationError
from bot.orders import place_order
from bot.logging_config import logger
import json

def format_output(title: str, data: dict):
    print(f"\n{'='*40}")
    print(f" {title} ")
    print(f"{'='*40}")
    print(json.dumps(data, indent=2))
    print(f"{'='*40}\n")

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--symbol", type=str, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", type=str, choices=["BUY", "SELL", "buy", "sell"], help="Order side (BUY or SELL)")
    parser.add_argument("--type", type=str, choices=["MARKET", "LIMIT", "market", "limit"], help="Order type (MARKET or LIMIT)")
    parser.add_argument("--quantity", type=str, help="Quantity to trade")
    parser.add_argument("--price", type=str, help="Price (required for LIMIT orders)")
    
    args = parser.parse_args()
    
    if args.interactive:
        print("\n--- Interactive Trading Mode ---")
        symbol = input("Enter symbol (e.g., BTCUSDT): ")
        side = input("Enter side (BUY or SELL): ")
        order_type = input("Enter order type (MARKET or LIMIT): ")
        quantity = input("Enter quantity: ")
        price = None
        if order_type and order_type.upper() == "LIMIT":
            price = input("Enter price: ")
    else:
        if not all([args.symbol, args.side, args.type, args.quantity]):
            parser.error("the following arguments are required: --symbol, --side, --type, --quantity. Or use --interactive")
        symbol = args.symbol
        side = args.side
        order_type = args.type
        quantity = args.quantity
        price = args.price
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Validate inputs
        validated_data = validate_order_input(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        # Print summary
        summary = {
            "Symbol": validated_data["symbol"],
            "Side": validated_data["side"],
            "Type": validated_data["order_type"],
            "Quantity": validated_data["quantity"]
        }
        if validated_data["price"]:
            summary["Price"] = validated_data["price"]
            
        format_output("Order Request Summary", summary)
        
        # Place order
        print("Placing order...")
        response = place_order(
            symbol=validated_data["symbol"],
            side=validated_data["side"],
            order_type=validated_data["order_type"],
            quantity=validated_data["quantity"],
            price=validated_data["price"]
        )
        
        # Format response
        if response:
            details = {
                "Order ID": response.get("orderId"),
                "Status": response.get("status"),
                "Executed Quantity": response.get("executedQty")
            }
            if response.get("avgPrice") and float(response.get("avgPrice")) > 0:
                details["Average Price"] = response.get("avgPrice")
                
            format_output("Order Response Details", details)
            print("SUCCESS: Order placed successfully!\n")
            
    except ValidationError as e:
        print(f"\nERROR (Validation): {e}\n")
    except Exception as e:
        print(f"\nERROR (Execution): {e}\n")

if __name__ == "__main__":
    main()
