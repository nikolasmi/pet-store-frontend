export interface Review {
    reviewId: number
    userId: number
    petId: number
    rating: number
    comment: string
    pet: Pet
    user: User
}
  
export interface Pet {
    petId: number
    name: string
    description: string
    type: string
    age: number
    size: string
    origin: string
    price: number
    availabe: string
    imagePath: string
}
  
export interface User {
    userId: number
    email: string
    pasword: string
    name: string
    phone: string
    address: string
    favoriteType: string
}