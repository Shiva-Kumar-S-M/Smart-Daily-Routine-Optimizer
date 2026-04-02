# movie_booking_system.py

class Movie:
    def __init__(self, title, genre, duration):
        self.title = title
        self.genre = genre
        self.duration = duration

    def display_movie_details(self):
        return f"Title: {self.title}, Genre: {self.genre}, Duration: {self.duration} minutes"

class Theater:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.movies_playing = {}
        self.showtimes = {}
        self.bookings = []

    def add_movie(self, movie, showtime):
        if movie.title not in self.movies_playing:
            self.movies_playing[movie.title] = movie
            self.showtimes[movie.title] = [showtime]
        else:
            self.showtimes[movie.title].append(showtime)

    def display_available_movies(self):
        if not self.movies_playing:
            return "No movies currently playing."
        details = [f"Available movies at {self.name}:"]
        for title, movie in self.movies_playing.items():
            details.append(f"- {movie.display_movie_details()} (Showtimes: {', '.join(self.showtimes[title])})")
        return "\n".join(details)

    def book_ticket(self, movie_title, showtime, num_tickets):
        if movie_title not in self.movies_playing:
            return "Movie not found."
        if showtime not in self.showtimes[movie_title]:
            return "Showtime not available."

        # Simple capacity check (can be improved with seat management)
        current_bookings_for_showtime = sum(b.num_tickets for b in self.bookings if b.movie_title == movie_title and b.showtime == showtime)
        if (current_bookings_for_showtime + num_tickets) > self.capacity:
            return "Not enough seats available."

        booking = Booking(movie_title, showtime, num_tickets, self.name)
        self.bookings.append(booking)
        return f"Booking successful! {num_tickets} tickets for {movie_title} at {showtime} in {self.name}."

class Booking:
    def __init__(self, movie_title, showtime, num_tickets, theater_name):
        self.movie_title = movie_title
        self.showtime = showtime
        self.num_tickets = num_tickets
        self.theater_name = theater_name

    def display_booking_details(self):
        return f"Booked {self.num_tickets} tickets for {self.movie_title} at {self.showtime} in {self.theater_name}."

# Interactive part
def main_menu():
    # Initialize movies and theaters
    movie1 = Movie("The Great Adventure", "Action", 120)
    movie2 = Movie("Love in Paris", "Romance", 95)
    movie3 = Movie("Mystery of the Old House", "Thriller", 110)

    cineplex = Theater("Cineplex", 50)
    grand_cinema = Theater("Grand Cinema", 30)

    cineplex.add_movie(movie1, "10:00 AM")
    cineplex.add_movie(movie1, "02:00 PM")
    cineplex.add_movie(movie2, "07:00 PM")

    grand_cinema.add_movie(movie3, "01:00 PM")
    grand_cinema.add_movie(movie1, "04:00 PM")

    theaters = {"Cineplex": cineplex, "Grand Cinema": grand_cinema}

    while True:
        print("\n--- Movie Booking System ---")
        print("1. View available movies")
        print("2. Book tickets")
        print("3. View my bookings")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            print("\n--- Available Movies ---")
            for theater_name, theater in theaters.items():
                print(theater.display_available_movies())

        elif choice == '2':
            print("\n--- Book Tickets ---")
            print("Available Theaters:")
            for i, name in enumerate(theaters.keys()):
                print(f"{i+1}. {name}")
            
            try:
                theater_choice = int(input("Select a theater by number: ")) - 1
                theater_name = list(theaters.keys())[theater_choice]
                selected_theater = theaters[theater_name]
            except (ValueError, IndexError):
                print("Invalid theater selection.")
                continue

            print(selected_theater.display_available_movies())
            movie_title = input("Enter the title of the movie you want to book: ")
            showtime = input("Enter the showtime (e.g., 10:00 AM): ")
            
            try:
                num_tickets = int(input("Enter the number of tickets: "))
                if num_tickets <= 0:
                    print("Number of tickets must be positive.")
                    continue
            except ValueError:
                print("Invalid number of tickets.")
                continue

            result = selected_theater.book_ticket(movie_title, showtime, num_tickets)
            print(result)

        elif choice == '3':
            print("\n--- My Bookings ---")
            found_bookings = False
            for theater_name, theater in theaters.items():
                if theater.bookings:
                    found_bookings = True
                    print(f"Bookings for {theater_name}:")
                    for booking in theater.bookings:
                        print(f"- {booking.display_booking_details()}")
            if not found_bookings:
                print("No bookings yet.")

        elif choice == '4':
            print("Exiting Movie Booking System. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()

class Solution:
    def maximumAmount(self, coins):
        m,n=len(coins),len(coins[0])
        NEG=float('-inf')
        dp=[[NEG]*3 for _ in range(n)]

        for k in range(3):
            dp[0][k]=max(coins[0][0],0) if k>0 else coins[0][0]

        for j in range(1,n):
            for k in range(2,-1,-1):
                dp[j][k]=max(dp[j][k], dp[j-1][k]+coins[0][j])
                if k>0:
                    dp[j][k]=max(dp[j][k], dp[j-1][k-1])

        for i in range(1,m):
            ndp=[[NEG]*3 for _ in range(n)]
            for j in range(n):
                for k in range(2,-1,-1):
                    if dp[j][k]!=NEG:
                        ndp[j][k]=max(ndp[j][k], dp[j][k]+coins[i][j])
                    if k>0 and dp[j][k-1]!=NEG:
                        ndp[j][k]=max(ndp[j][k], dp[j][k-1])
                    if j>0:
                        if ndp[j-1][k]!=NEG:
                            ndp[j][k]=max(ndp[j][k], ndp[j-1][k]+coins[i][j])
                        if k>0 and ndp[j-1][k-1]!=NEG:
                            ndp[j][k]=max(ndp[j][k], ndp[j-1][k-1])
            dp=ndp

        return dp[n-1][2]
