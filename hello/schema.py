from graphene_django import DjangoObjectType
from django.contrib.auth.models import User as UserModel
import graphene


class User(DjangoObjectType):
    class Meta:
        model = UserModel


class Query(graphene.ObjectType):
    users = graphene.List(User)

    @graphene.resolve_only_args
    def resolve_users(self):
        return UserModel.objects.all()


class PersonInput(graphene.InputObjectType):
    email = graphene.String()


class ChangePerson(graphene.Mutation):

    class Input:
        name = graphene.String()
        person_data = graphene.Argument(PersonInput)

    ok = graphene.Boolean()
    user = graphene.Field(lambda: User)

    @staticmethod
    def mutate(root, args, context, info):
        person_data = args['person_data']
        user = UserModel.objects.get(username=args.get('name'))
        user.email = person_data['email']
        user.save()
        ok = True
        return ChangePerson(user=user, ok=ok)


class Mutations(graphene.ObjectType):
    change_person = ChangePerson.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
